import os

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from gallery import get_db_images_tag
from database.db import get_collection
from config import get_image_dir

templates = Jinja2Templates(directory="../templates")
router = APIRouter()
collection = get_collection()
IMAGE_DIR = get_image_dir()


@router.get("/gallery", response_class=HTMLResponse)
async def gallery(request: Request):
    db_data = get_db_images_tag()
    return templates.TemplateResponse("gallery.html", {"request": request, "data": db_data})

@router.get("/view")
def view(request: Request, image_id: str = None):
    db_data = get_db_images_tag()
    return templates.TemplateResponse("image_view.html", {"request": request, "data": db_data, "selected_image_id": image_id})



""" To edit or delete image in the gallery
    edit route
    delete route
"""

@router.put("/update-image/{image_id}")
async def update_image(image_id: str, request: Request):
    try:
        data = await request.json()
        print("Received update data:", data)  # Debug log
        
        # Get existing metadata
        existing = collection.get(ids=[image_id])
        existing_metadata = existing['metadatas'][0]
        
        # Update only provided fields
        updated_metadata = {
            "description": data.get("description", existing_metadata.get("description", "")),
            "tags": ",".join(data.get("tags", existing_metadata.get("tags", "").split(','))),
            "date": data.get("date", existing_metadata.get("date", "")),
            "path": existing_metadata.get("path", "")
        }
        
        collection.update(
            ids=[image_id],
            metadatas=[updated_metadata]
        )
        return {"status": "success"}
    except Exception as e:
        print("Update error:", str(e))  
        raise HTTPException(status_code=400, detail=str(e))




@router.delete("/delete-image/{image_id}")
async def delete_image(image_id: str):
    try:
        # 1. Get existing record to find file path
        existing = collection.get(ids=[image_id])
        if not existing["ids"]:
            raise HTTPException(status_code=404, detail="Image not found in database")
            
        # 2. Extract file path from metadata
        metadata = existing["metadatas"][0]
        image_path = metadata.get("path", "")
        
        if image_path:
            # 3. Security check and path resolution
            safe_path = os.path.abspath(os.path.join(IMAGE_DIR, image_path))
            
            # Prevent directory traversal attacks
            if not safe_path.startswith(os.path.abspath(IMAGE_DIR)):
                raise HTTPException(status_code=400, detail="Invalid image path")
            
            # 4. Delete physical file
            if os.path.exists(safe_path):
                try:
                    os.remove(safe_path)
                except Exception as file_error:
                    raise HTTPException(
                        status_code=500, 
                        detail=f"File deletion failed: {str(file_error)}"
                    )
            else:
                print(f"Warning: File not found at {safe_path}")

        # 5. Delete database record
        collection.delete(ids=[image_id])
        
        return {"status": "success", "message": "Image and record deleted successfully"}
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))