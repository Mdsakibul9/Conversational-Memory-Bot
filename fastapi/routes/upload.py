import os
import uuid
import shutil
from fastapi import APIRouter, Request, UploadFile, File, Query, HTTPException
from fastapi.responses import  RedirectResponse
from fastapi.templating import Jinja2Templates

from config import get_image_dir
from database.db import add_image
from static.string_file import UploadStr
# Set up static paths and templates
IMAGE_DIR = get_image_dir()
templates = Jinja2Templates(directory="../templates")

router = APIRouter()


@router.get("/upload")
async def show_upload_form(request: Request, success: str = Query(None)):
    return templates.TemplateResponse(
        "upload.html",{"request": request,"success": success})


@router.post("/upload")
async def upload_images(files: list[UploadFile] = File(...)):
    try:
        for file in files:
            # Generate a unique ID for the image.
            unique_id = str(uuid.uuid4())
            filename = unique_id + "_" + file.filename
            file_location = os.path.join(IMAGE_DIR , filename)
            
            # Save the uploaded file.
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                
            # Call db function to add the image embedding and metadata
            await add_image(file_location, filename, unique_id)
            
        return RedirectResponse(url=UploadStr.SUCCESS_MESSAGE , status_code=303)

    except Exception as e:
        raise KeyError(UploadStr.ERROR_ADDING_TO_VECTOR_DB.format(str(e)))