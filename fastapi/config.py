import os
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai


from history import ConversationHistory
from static.string_file import ConfigStrings

# Load environment variables from .env file
load_dotenv("./.env")

# Instantiate conversation history with a max size of 6
conversation_dir = os.path.join(os.path.dirname(__file__), "static")
conversation_history = ConversationHistory(conversation_dir, max_size=6)


def get_image_dir(directory: str = "images"):
    """Create or retrieve the image directory and return its Path object."""
    image_dir = Path(directory)
    try:
        if not image_dir.exists():
            os.makedirs(image_dir)
            print(ConfigStrings.DIR_CREATED_MESSAGE.format(dir_path=image_dir))
        else:
            print(ConfigStrings.DIR_EXISTS_MESSAGE.format(dir_path=image_dir))
    except OSError as error:
        print(ConfigStrings.DIR_ERROR_MESSAGE.format(dir_path=image_dir, error=error))
    
    return image_dir


# Vector Database Configuration 
def db_configuration() -> str:
    """Configure and return the persistence directory for the vector database."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    persist_dir = os.path.join(base_dir, "chroma_db")
    
    if not os.path.exists(persist_dir):
        os.makedirs(persist_dir)
    
    return persist_dir



# Configure the Generative AI client using API key & using gemini-2.0-flash-exp model
def get_model():
    """Configure and return the generative AI model using the Gemini API."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(ConfigStrings.API_KEY_ERROR_MESSAGE)
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
    return model



if __name__ == "__main__":
    # Create the directory and store the path in a variable
    IMAGE_DIR = get_image_dir()
    # create the persistence directory 
    PERSIST_DIR = db_configuration()
    # get the model
    model = get_model()