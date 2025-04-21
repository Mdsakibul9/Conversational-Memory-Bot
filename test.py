# 1. First install required packages
# pip install chromadb openclip-torch pillow

import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from PIL import Image
import numpy as np
import torch 
import clip

from ./fastapi.call_llm import descriptions





device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_image_embedding(image_path: str):
    try:
        # Open and prepare the image
        image = Image.open(image_path).convert("RGB")
        image_input = preprocess(image).unsqueeze(0).to(device)
        with torch.no_grad():
            embedding = model.encode_image(image_input)
        embedding_list = embedding[0].cpu().tolist()
    except Exception as e:
        print(f"Error procesasing the image {image_path}: {str(e)}")
        raise 
    return embedding_list


# --- Database Functions ---
def add_image(image_path, metadata, image_id):
    """
    Adds an image (its embedding and associated metadata) to the Chroma DB.
    
    Parameters:
      - image_path: Path to the image file.
      - metadata: A dictionary containing any additional information (e.g., description, context, named entities).
      - image_id: A unique identifier for the image.
    """
    print(image_path)
    # Compute the image embedding.
    embedding = get_image_embedding(image_path)
    
    # Optionally, you can store the image file path or a thumbnail as the document.
    # Here, we simply store the file path as the "document" field.
    document = image_path
    
    
    print(embedding)
    
    # collection = {
    #     'embeddings'=[embedding],
    #     'documents'=[document],
    #     'metadatas'= [metadata],
    #     'ids'=[image_id]
    # }
    # print(collection)
    
add_image("C:\\Users\\BJIT\\Downloads\\street.jpg",{"context"}, "image123")