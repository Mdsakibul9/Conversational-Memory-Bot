import os
import io
import uuid
import base64



from fastapi import APIRouter, Request, HTTPException,File, Form, HTTPException,UploadFile 
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from PIL import Image

from config import conversation_history
from backend_llm.llm import chatbot
from static.string_file import RouteChat

templates = Jinja2Templates(directory="../templates")
router = APIRouter()

# To iterate through the different type of output generated by different llm functions
def chatbot_output_iterator(user_text=None, user_image=None):
    """
    Processes chatbot results into a tuple of one description and multiple image paths,
    storing IDs in conversation history. Can work with list and string type of data also.
    """
    results = chatbot(user_text, user_image)
    descriptions = []
    image_paths = []
    
    if isinstance(results, dict):
        descriptions.append(results.get("description", "No description provided"))
        image_paths.extend(results.get("path", []))
        image_ids = results.get("id", [])
        # Use the conversation history manager to add bot message
        conversation_history.add_bot_message(
            results.get("description", "No description provided"),
            image_paths,
            image_ids
        )
    
    elif isinstance(results, str):
        descriptions.append(results)
        conversation_history.add_bot_message(results, [], [])
    
    
    elif isinstance(results, list):
        for item in results:
            if isinstance(item, tuple) and len(item) == 3:
                description, image_path, _ = item
                descriptions.append(description)
                if image_path:
                    image_paths.append(image_path)
            elif isinstance(item, str):
                descriptions.append(item)
        conversation_history.add_bot_message("\n".join(descriptions), image_paths, [])
    
    else:
        descriptions.append(RouteChat.UNEXPECTED_RESPONSE)
        conversation_history.add_bot_message(RouteChat.UNEXPECTED_TYPE_RESPONSE, [], [])
    
    combined_description = "\n".join(descriptions)
    return (combined_description, image_paths)


# Route for the chatbot query
@router.post("/query", response_class=HTMLResponse)
async def query(request: Request,query_text: str = Form(None),image: list[UploadFile] = File(None)):
    if not query_text and not image:
        return HTMLResponse(content='<div class="error">Please provide text or upload images.</div>', status_code=400)

    query_images = []
    image_pil_list = []
    if image:
        for img in image:
            if img.filename:
                try:
                    image_data = await img.read()
                    image_pil = Image.open(io.BytesIO(image_data)).convert("RGB")
                    image_pil_list.append(image_pil)
                    buffered = io.BytesIO()
                    image_pil.save(buffered, format="JPEG")
                    base64_data = base64.b64encode(buffered.getvalue()).decode()
                    query_images.append(base64_data)
                except Exception:
                    raise HTTPException(status_code=400, detail="Invalid image file")

    user_message_id = str(uuid.uuid4())

    user_image_pil = image_pil_list[0] if image_pil_list else None
    combined_description, image_paths = chatbot_output_iterator(query_text, user_image_pil)

    bot_message_id = str(uuid.uuid4())
    bot_images = [os.path.basename(path) for path in image_paths if path]
    bot_message = {
        "role": "bot",
        "text": combined_description,
        "images": bot_images,
        "id": bot_message_id
    }
    
    # Use the conversation history manager to add a user message
    conversation_history.add_user_message(query_text)
    
    # Return only the bot message
    bot_html = f'<div class="message bot" data-id="{bot_message_id}"><p>{bot_message["text"]}</p>'
    if bot_message["images"]:
        bot_html += '<div class="image-row">'
        for img in bot_message["images"]:
            bot_html += f'<img src="/images/{img}" alt="Response Image">'
        bot_html += '</div>'
    bot_html += '</div>'

    # Return a JSON response with both the bot HTML and the user_message_id
    return JSONResponse(content={
        "bot_html": bot_html,
        "user_message_id": user_message_id
    })


@router.post("/clear", response_class=HTMLResponse)
async def clear_chat(request: Request):
    # Use conversation history manager to clear history
    conversation_history.clear()
    return HTMLResponse(content='<p style="text-align: center; color: #888;">Start a conversation below!</p>')


@router.get("/chat", response_class=HTMLResponse)
async def root(request: Request):
    # Retrieve conversation from history manager
    history = conversation_history.get_history()
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "conversation": history
    })




