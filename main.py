from fastapi import FastAPI
from src.api.routes import router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Automotive Ergonomics Multimodal RAG",
    description="A production-grade RAG system for automotive engineering documents.",
    version="1.0.0"
)

app.include_router(router)

@app.get('/')
async def root():
    return {
        'message': 'Welcome to the Automotive Ergonomics Multimodal RAG API',
        'documentation': '/docs',
        'health': '/health'
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
