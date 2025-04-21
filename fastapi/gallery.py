from database.db import get_collection


collection = get_collection()

# Retrieve the images and descriptions from the database
def get_db_images_tag():
    data = collection.get()
    ids = data["ids"][::-1]  
    description = [m_data.get("description", "No Description Available") for m_data in data["metadatas"]][::-1]
    file_paths = [m_data.get("path", "") for m_data in data["metadatas"]][::-1]
    tags_list = [m_data.get("tags", "").split(",") if "tags" in m_data else [] for m_data in data["metadatas"]][::-1]
    dates = [m_data.get("date", "") for m_data in data["metadatas"]][::-1]
    return zip(ids, description, file_paths, tags_list, dates)









