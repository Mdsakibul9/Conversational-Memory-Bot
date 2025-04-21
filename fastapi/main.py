from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import database functions and query functions

from config import get_image_dir


app = FastAPI()
IMAGE_DIR = get_image_dir()
templates = Jinja2Templates(directory="../templates")
app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")
app.mount("/static", StaticFiles(directory="static"), name = "static")

# Import your route modules
from routes.home import router as home_router
from routes.gallery import router as gallery_router
from routes.upload import router as upload_router
from routes.search import router as search_router
from routes.chat import router as chat_router

app.include_router(home_router)
app.include_router(gallery_router)
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(chat_router)


















