# IntelliDoc: Document Processing & RAG Chatbot System

A Django-based system that combines document processing capabilities with a RAG (Retrieval-Augmented Generation) chatbot service. The system processes various document formats, creates embeddings, and enables interactive conversations with document content.

![Screenshot from 2024-10-29 16-11-21-1](https://github.com/user-attachments/assets/16804961-6fc9-4277-8b8a-f20bd09542b1)

RESTful APIs:
> https://www.postman.com/noire-aashish-nk/workspace/intellidoc-api/collection/28604040-8978b6ad-39f6-48d5-a37a-24eb6eb51d93?action=share&creator=28604040

## Features

- **Document Processing Service**
  - Support for multiple file formats (.txt, .pdf, .doc, .docx)
  - Automatic text extraction and embedding generation
  - Vector database storage using ChromaDB
  - Asynchronous processing using Celery
  - Unique asset ID generation for each document

- **RAG Chatbot Service**
  - Real-time chat interface using WebSocket
  - Support for multiple concurrent chat threads
  - Chat history tracking and retrieval
  - Stream-based response generation
  - Integration with LangChain for document retrieval

## System Requirements

- Python 3.8+
- Redis Server
- Virtual Environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
SECRET_KEY=your_django_secret_key
OPENAI_API_KEY=your_openai_api_key
```

5. Initialize the database:
```bash
python manage.py migrate
```

6. Start Redis server:
```bash
redis-server
```

7. Start Celery worker:
```bash
celery -A document_processor worker --loglevel=info
```

8. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Document Processing

- **POST** `/api/documents/process/`
  - Accepts multipart form data with a file
  - Returns a task ID for tracking the processing status
  - Supported file types: .txt, .pdf, .doc, .docx

### Chat Interface

- **POST** `/api/chat/start/`
  - Input: `{"asset_id": "string"}`
  - Returns: `{"thread_id": "string"}`

- **POST** `/api/chat/message/`
  - Input: `{"thread_id": "string", "user_message": "string"}`
  - Returns: Streamed response from the chatbot

- **GET** `/api/chat/history/`
  - Query parameter: `thread_id`
  - Returns: Array of chat messages with timestamps

### WebSocket Connection

- **WS** `/ws/chat/<thread_id>/`
  - Establishes real-time chat connection
  - Handles message streaming and updates

## Project Structure

```
├── chat/                   # Chat application
│   ├── consumers.py       # WebSocket consumers
│   ├── models.py          # Chat models
│   ├── utils.py           # Chat utilities
│   └── views.py           # Chat views
├── processor/             # Document processing application
│   ├── tasks.py          # Celery tasks
│   ├── utils.py          # Processing utilities
│   └── views.py          # Processing views
└── document_processor/    # Project configuration
    ├── celery.py         # Celery configuration
    └── settings.py       # Django settings
```

## Technologies Used

- **Backend Framework**: Django & Django REST Framework
- **WebSocket**: Django Channels
- **Task Queue**: Celery
- **Message Broker**: Redis
- **Vector Database**: ChromaDB
- **Machine Learning**: LangChain, HuggingFace Embeddings
- **Document Processing**: PyPDF2, python-docx

## Error Handling

The system includes comprehensive error handling for:
- Invalid file types
- Processing failures
- Missing documents
- Invalid chat threads
- WebSocket connection issues

## Performance Considerations

- Asynchronous document processing using Celery
- Efficient vector storage and retrieval using ChromaDB
- WebSocket-based real-time communication
- Streaming responses for better user experience

## Security Measures

- CSRF protection enabled
- File type validation
- Secure WebSocket connections
- Environment variable management
- Input sanitization

## Development

To contribute to the project:

1. Create a new branch for your feature
2. Write tests for new functionality
3. Ensure code follows PEP 8 style guide
4. Submit a pull request with detailed description

## Testing

Run tests using:
```bash
python manage.py test
```

## Deployment Considerations

- Configure ALLOWED_HOSTS in settings.py
- Set DEBUG=False in production
- Use proper WSGI/ASGI server (e.g., Gunicorn, Daphne)
- Set up proper SSL/TLS certificates
- Configure production-grade databases
- Set up proper logging
