# Standard Library Imports
import os
import logging
import json
from datetime import datetime

import chromadb
from chromadb.utils.data_loaders import ImageLoader
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from fastapi import HTTPException

from backend_llm.call_llm import description
from config import db_configuration
from static.string_file import VectorDBStrings

# Configure a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PERSIST_DIR = db_configuration()
# Create The client
def get_client():
    DIR = PERSIST_DIR
    client = chromadb.PersistentClient(path=DIR)
    return client


# Create or get the collection where image embeddings will be stored.
def get_collection():
    # Get the client 
    client = get_client()
        
    # For Funcationality
    embedding_function = OpenCLIPEmbeddingFunction()
    image_loader = ImageLoader()
    collection = client.get_or_create_collection(
        name="image_embeddings",
        embedding_function=embedding_function,
        data_loader=image_loader
    )
    return collection


# Add image in the vector database
async def add_image(image_add_path,image_path, image_id):
    """
    Add an image (its embedding and metadata) to the ChromaDB collection.

    Args:
        image_add_path: Path to the image file to be added.
        image_path: Path metadata for the image.
        image_id: Unique identifier for the image.

    Raises:
        HTTPException: If the image file is not found (404) or an error occurs (500).
    """
    if not os.path.exists(image_add_path):
        raise FileNotFoundError(VectorDBStrings.IMAGE_NOT_FOUND_ERROR.format(image_path=image_add_path))
    
    try:
        # Generate a description for the image using description function.
        result = await description(image_add_path)
        response_text = result.replace('```json', '').replace('```', '').strip()
        output = json.loads(response_text)
        description_text = output.get("description")
        tags = output.get("tags")
        tags_str = ", ".join(tags)
        logger.info(VectorDBStrings.DESCRIPTION_LOG.format(image_id=image_id, description=description_text))

        collection = get_collection()
        date_str = datetime.now().strftime("%Y-%m-%d")
        logger.info(VectorDBStrings.ADDING_IMAGE_LOG.format(image_id=image_id, date=date_str))
        
        # Add the image to the collection.
        collection.add(
            ids=[image_id],
            uris=[image_add_path],
            metadatas=[{"path": image_path, "description": description_text, "tags": tags_str, "date":date_str}],
        )
        
        logger.info(VectorDBStrings.SUCCESS_LOG.format(image_id=image_id))
    
    except FileNotFoundError as fnf_error:
        logger.error(VectorDBStrings.FILE_NOT_FOUND_LOG.format(image_id=image_id, error=fnf_error))
        raise HTTPException(status_code=404, detail=str(fnf_error))
    except Exception as error:
        logger.error(VectorDBStrings.GENERAL_ERROR_LOG.format(image_id=image_id, error=error), exc_info=True)
        raise HTTPException(status_code=500, detail=str(error))

    
