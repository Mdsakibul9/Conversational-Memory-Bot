import io
from PIL import Image
from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database.db_query import text_query, image_query

templates = Jinja2Templates(directory="../templates")
router = APIRouter()

@router.get("/search")
async def search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@router.post("/search_image",response_class=HTMLResponse)
async def search_image(request: Request, image: UploadFile = File(...), n: int = Form(1)):
    # Read and open the uploaded image
    image_data = await image.read()
    image_pil = Image.open(io.BytesIO(image_data)).convert("RGB")
    
    # Call the query_image function to retrieve similar imagesS.
    retrieved = image_query(image_pil, n)
    result = []
    path = []
    for  meta in (retrieved['metadatas'][0]):
        result.append(meta.get('description'))
        path.append(meta.get('path'))
    
    image_info = zip(result, path)
    return templates.TemplateResponse("search.html", {"request": request, "image_info": image_info})
    

@router.post("/search_text",response_class=HTMLResponse,)
async def search_text(request: Request, text: str = Form(...),n: int = Form(1)):
    # Call the query_text function to retrieve images based on text.
    retrieved = text_query(text, n)
    result = []
    path = []
    for  meta in (retrieved['metadatas'][0]):
        result.append(meta.get('description'))
        path.append(meta.get('path'))
        
    image_info = zip(result, path)
    return templates.TemplateResponse("search.html", {"request": request, "image_info": image_info})