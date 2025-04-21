import numpy as np

# Local Application Imports
from database.db import get_collection

collection = get_collection()



def text_query(text, n_query=1):
    retrieved = collection.query(query_texts=[text], include=['metadatas','distances'], n_results=n_query)
    return retrieved

def image_query(img, n_query=5):
    query_image = np.array(img)
    retrieved = collection.query(query_images=[query_image], include=['metadatas','distances'], n_results=n_query)
    return retrieved
  



