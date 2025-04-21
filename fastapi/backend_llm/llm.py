import json
from typing import Any

from PIL import Image

from backend_llm.call_llm import description_image, general_chat,process_memory_query
from database.db_query import text_query, image_query
from config import get_model, conversation_history
from database.db import get_collection
from static.string_file import ChatbotStrings



# Initialize global instances
model = get_model()
collection = get_collection()


def analyze_intent(qtext):
    """
    Analyzes the provided user text to determine the intent.

    Returns:
        dict: A JSON object with:
            - "intent": one of ["query", "description", "memory", "chat"]
            - "refined_query": a refined query string if intent is "query" or "description", otherwise null.
    """
    # Defined the user prompt text
    prompt_text = (
        f"User text: '{qtext}'\n\n"
        "Instructions:\n"
        "You are a helpful expert AI Photo Bot. Analyze the provided user text. Determine the user's intent based on these criteria:\n" # Instructions are now part of the user prompt
        "1. 'query': The user is asking to give, show, retrieve, similar images or only entity name or give image descriptionns or some entity.\n"
        "2. 'description': The user wants an image description generated which is not a query.\n"
        "3. 'memory': The user refers to a past chat, query or past-conversation context.sentence would be in past tense or words like chat, conversation would be mentioned\n"
        "4. 'chat': The user is engaging in general conversation (e.g., about the website or photo gallery bot).\n\n"
        "Return a JSON object with:\n"
        "- 'intent': one of ['query', 'description', 'memory', 'chat']\n"
        "- 'refined_query': (if intent is 'query' or 'description') a refined query optimized for vector search; otherwise null.\n\n"
        "Output must only the JSON response with no additional commentary."
    )


    # Prepare the conversation for the model - NO system role now
    contents = [
        {
            "role": "user", 
            "parts": [
                {"text": prompt_text}
            ]
        }
    ]

    # Generate the response
    try:
        response = model.generate_content(contents)
        if response and response.text:
            response_text = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(response_text)
        else:
            print("No response received from Backend API.")
            return {"intent": "chat", "refined_query": None}
    except Exception as e:
        print(f"Error in analyze_intent: {e}")
        return {"Error in running the analylze intent function"}


# To add context for the llm . history has been expanding.
def expand_conversation_history(history: list[dict]) -> str:
    """
    Expand conversation history into a detailed, structured string for LLM context.

    Args:
        history: List of conversation entries from ConversationHistory.get_history().

    Returns:
        A formatted string with numbered chats and images for clear LLM referencing.
    """
    if not history:
        return ChatbotStrings.NO_HISTORY_AVAILABLE

    context = ChatbotStrings.HISTORY_CONTEXT_HEADER + "\n"
    for chat_idx, entry in enumerate(history, 1):
        role = entry.get('role', 'unknown')
        text = entry.get('text', 'No text provided')
        image_paths = entry.get('image_paths', [])
        image_ids = entry.get('image_ids', [])  
        timestamp = entry.get('timestamp', 'Unknown time')
        
        context += f"{ChatbotStrings.CHAT_ENTRY_FORMAT.format(chat_idx=chat_idx, timestamp=timestamp)}\n"
        context += f"{ChatbotStrings.ROLE_TEXT_FORMAT.format(role=role.capitalize(), text=text)}\n"
        
        if image_paths:
            context += ChatbotStrings.ASSOCIATED_IMAGES_HEADER + "\n"
            for img_idx, (path, img_id) in enumerate(zip(image_paths, image_ids or [None] * len(image_paths)), 1):
                context += f"{ChatbotStrings.IMAGE_ENTRY_FORMAT.format(img_idx=img_idx, path=path)}"
                if img_id:
                    context += f"{ChatbotStrings.IMAGE_ID_FORMAT.format(img_id=img_id)}"
                if path not in text:
                    context += ChatbotStrings.IMAGE_NOT_DESCRIBED
                context += "\n"
        context += "\n"
    
    return context.strip()


def generate_query_expansion_and_clarification(qtext: str, image: Image.Image) -> dict:
    """Generate an expanded query and check for ambiguities based on text and image."""
    response = model.generate_content([
        image,
        ChatbotStrings.IMAGE_CONTEXT,
        qtext,
        ChatbotStrings.TEXT_CONTEXT,
        ChatbotStrings.QUERY_EXPANSION_INSTRUCTION,
        ChatbotStrings.QUERY_EXPANSION_OUTPUT
    ])

    try:
        if response and response.text:
            response_text = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(response_text)
        else:
            print(ChatbotStrings.NO_RESPONSE_ERROR)
            return ChatbotStrings.DEFAULT_CHAT_RESPONSE
    except Exception as error:
        print(f"Error in analyze_intent: {error}")
        return {"error": ChatbotStrings.INTENT_ERROR}


def generate_query_expansion_and_clarification_using_text(qtext: str, history_context) -> dict:
    """Generate an expanded query and check for ambiguities based on text only."""
    prompt = ChatbotStrings.TEXT_ONLY_EXPANSION_PROMPT.format(qtext=qtext, history_context=history_context)
    response = model.generate_content([prompt])
    print("text query expansion", response.text)

    response_text = response.text.replace('```json', '').replace('```', '').strip()
    print(response_text)
    try:
        return json.loads(response_text)
    except json.JSONDecodeError as error:
        print(ChatbotStrings.INVALID_JSON_ERROR.format(response_text=response_text))
        return json.loads(ChatbotStrings.JSON_DECODE_ERROR_RESPONSE.format(error=str(error)))


def format_retrieved_images(retrieved: dict) -> str:
    """Format retrieved image data from ChromaDB into a text string."""
    ids = retrieved.get('ids', [[]])[0]
    metadatas = retrieved.get('metadatas', [[]])[0]
    distances = retrieved.get('distances', [[]])[0]

    retrieved_text = ""
    for idx in range(len(ids)):
        img_id = ids[idx]
        metadata = metadatas[idx] if idx < len(metadatas) else {}
        distance = distances[idx] if idx < len(distances) else float('inf')
        path = metadata.get('path', 'unknown_path')
        description = metadata.get('description', ChatbotStrings.NO_DESCRIPTION_AVAILABLE)
        tags = metadata.get('tags', '')
        retrieved_text += (
            f"Image ID: {img_id}\n"
            f"Path: {path}\n"
            f"Description: {description}\n"
            f"Distance: {distance:.2f}\n"
            f"Tags: {tags}\n\n"
        )

    return retrieved_text.strip() if retrieved_text.strip() else ChatbotStrings.NO_IMAGE_RETRIEVED

def generate_augmented_response(user_query: str, retrieved: dict, num_requested: int) -> dict:
    """Generate a JSON-formatted response based on user query and retrieved images."""
    retrieved_text = format_retrieved_images(retrieved)
    prompt = ChatbotStrings.AUGMENTED_RESPONSE_PROMPT.format(
        user_query=user_query,
        num_requested=num_requested,
        retrieved_text=retrieved_text
    )
    try:
        response = model.generate_content([prompt])
        response_text = response.text.replace('```json', '').replace('```', '').strip()
        print(response_text)
        return json.loads(response_text)
    except Exception:
        return ChatbotStrings.AUGMENTED_RESPONSE_ERROR


def generate_augmented_response_from_image(user_image: Image.Image, retrieved: dict) -> dict:
    """Generate a JSON-formatted response based on a user-uploaded image and retrieved images."""
    retrieved_text = format_retrieved_images(retrieved)
    prompt = ChatbotStrings.AUGMENTED_IMAGE_RESPONSE_PROMPT.format(
        retrieved_text=retrieved_text,
        user_image=user_image
    )
    try:
        response = model.generate_content([prompt])
        response_text = response.text.replace('```json', '').replace('```', '').strip()
        print(response_text)
        return json.loads(response_text)
    except Exception:
        return ChatbotStrings.AUGMENTED_IMAGE_RESPONSE_ERROR


def handle_query(qtext: str, image: Image.Image | None, history_context) -> list[Any | None] | dict | None:
    """Handle query processing based on text and optional image input."""
    if qtext and image is None:
        query_expansion = generate_query_expansion_and_clarification_using_text(qtext, history_context)
        expanded_qry = query_expansion.get("expanded_query")
        flag = query_expansion.get("ambiguous")
        message = query_expansion.get("message")
        result = []
        if flag:
            result.append(message)
        else:
            n = int(query_expansion.get("num_images_requested", 1))
            if n > 5:
                n = 5
            received = text_query(expanded_qry, n)
            return generate_augmented_response(qtext, received, n)
        print(result)
        return result
    elif image and qtext:
        query_expansion = generate_query_expansion_and_clarification(qtext, image)
        print(query_expansion)
        expanded_qry = query_expansion.get("expanded_query")
        flag = query_expansion.get("ambiguous")
        result = []
        message = query_expansion.get("message")
        if flag:
            result.append(message)
        else:
            n = int(query_expansion.get("num_images_requested", 1))
            if n > 5:
                n = 5
            received = text_query(expanded_qry, n)
            return generate_augmented_response(expanded_qry, received, n)
        print(result)
        return result


def chatbot(user_text: str | None = None, user_image: Image.Image | None = None) -> str | list | dict:
    """Main chatbot function to process user text and/or image input."""
    history = conversation_history.get_last_n(5)
    history_context = expand_conversation_history(history)
    if user_text:
        intent = analyze_intent(user_text)
        if intent["intent"] == "query":
            return handle_query(user_text, user_image, history_context)
        elif intent["intent"] == "description":
            if user_image:
                return description_image(user_image)
            else:
                return general_chat(user_text, history_context)
        elif intent["intent"] == "memory":
            received = process_memory_query(user_text,history_context)
            return received
        elif intent["intent"] == "database":
            return ChatbotStrings.DATABASE_UNAVAILABLE
        else:
            return general_chat(user_text, history_context)
    else:
        received = image_query(user_image)
        return generate_augmented_response_from_image(user_image, received)


