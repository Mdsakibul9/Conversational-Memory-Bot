# Conversational Memory Bot – AI-Powered Photo Gallery Assistant

## Overview
A sophisticated FastAPI-based web application that integrates image management, vector database storage, and AI-powered chat functionalities using Google's Gemini model. This system enables users to upload, search, and interact with images via natural language queries, while maintaining conversation history for contextual responses.

## 🚀 Features
- **AI-Powered Image Analysis**: Automatically generates descriptions and tags for images using Gemini AI.
- **Vector Database Storage**: Efficiently stores and retrieves image data using ChromaDB.
- **Natural Language Processing**: Processes queries intelligently and manages conversations.
- **Image Gallery**: Allows visual browsing of uploaded images with their descriptions and tags.
- **Conversation Memory**: Retains chat history to provide context-aware responses.
- **Multi-Modal Interaction**: Supports queries via text and images.

## 🛠 Technology Stack
- **Backend**: FastAPI
- **AI Model**: Google Gemini 2.0
- **Vector Database**: ChromaDB
- **Image Processing**: Pillow (PIL)
- **Frontend**: HTML, CSS, JavaScript
- **Template Engine**: Jinja2

## 📋 Prerequisites
Before setting up the project, ensure you have:
- Python 3.8 or higher (3.12.5 preferred)
- A Google Cloud API key for Gemini AI
- Sufficient storage space for the image database
- Install required packages using requirements.txt

## ⚙️ Installation
Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd fastapi
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**: Create a .env file in the project root and add your Gemini API key:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

## 📁 Project Structure
Here's how the project is organized:

```
fastapi/
├── backend_llm/        # LLM integration and processing logic
├── database/           # Database operations and queries
├── routes/             # API endpoints and routing definitions
├── static/             # Static files (e.g history.json, string_files)
├── templates/          # HTML templates for the frontend
├── images/             # Directory for stored images
├── chroma_db/          # Vector database storage using ChromaDB
├── main.py             # Main Python Scripts
├── gallery.py          # retrive data for gallery
├── histroy.py          # To create the history.json for storage
└── config.py           # Configuration settings

```

## 🚀 Running the Application
To launch the application:

1. **Start the FastAPI Server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the Application**:
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

   Note: The API docs provide an interactive interface to explore and test endpoints.

## 🔧 API Endpoints
The application exposes the following endpoints:

### Image Management
- **POST /upload**: Upload new images for processing and storage.
- **GET /gallery**: Retrieve and display all uploaded images.
- **GET /search**: Search images by their descriptions or tags.

### Chat Interface
- **POST /query**: Submit text or image-based queries for processing.
- **POST /clear**: Reset the chat history.
- **GET /chat**: Access the chat interface.

## 💡 Usage Examples
Here are some practical examples of how to interact with the API:

### Image Upload
Upload an image to the system:
- **Request**: Send a POST request to `/upload` with the image file in the form data.
- **Behavior**: The image is processed by Gemini AI, tagged, and stored.

### Image Search
Search for images using a natural language query:
- **Request**: Send a POST request to `/query` with a JSON body:
  ```json
  {"query": "Show me images of mountains"}
  ```
- **Response**: Returns images matching the query based on descriptions or tags.

### Chat Interaction
Ask about previous interactions:
- **Request**: Send a POST request to `/query` with a JSON body:
  ```json
  {"query": "What was the last image we discussed about?"}
  ```
- **Response**: Provides a contextual answer based on chat history.

## 🤝 Contributing
We welcome contributions! To contribute:

1. Fork the repository on GitHub.
2. Create a feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add AmazingFeature'
   ```
4. Push to your branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request on GitHub.

## 📝 License
This project is licensed under the MIT License. See the LICENSE file for details.

## 👥 Authors
- MD Sakib Ul Islam
- Contact: sakib.islam@bjitacademy.com



## 🙏 Acknowledgments
- **Google Gemini AI**: For powering image analysis and processing.
- **ChromaDB**: For efficient vector database capabilities.
- **FastAPI Community**: For providing an excellent framework and support.
