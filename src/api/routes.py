from fastapi import APIRouter, HTTPException, UploadFile, File
from src.api.schemas import QueryRequest, QueryResponse, IngestResponse, HealthStatus, Citation, ConfigResponse
from src.utils.resource_manager import ResourceManager
from src.ingestion.parser import PDFParser
from src.retrieval.vector_store import FAISSStore
from src.models.local_llm import LocalLLM
import os
import shutil
import pdfplumber

router = APIRouter()
parser = PDFParser()
store = FAISSStore()
llm = LocalLLM()

@router.get('/health', response_model=HealthStatus)
async def health():
    return {
        'status': 'healthy',
        'resources': ResourceManager.get_resource_status(),
        'index_size': len(store.metadata)
    }

@router.get('/config', response_model=ConfigResponse)
async def config():
    return {
        'model_name': 'Qwen2.5-0.5B-Instruct',
        'embedding_model': 'all-MiniLM-L6-v2',
        'vector_store': 'FAISS',
        'version': '1.0.0'
    }

@router.post('/ingest', response_model=IngestResponse)
async def ingest(file: UploadFile = File(...)):
    os.makedirs('data/raw', exist_ok=True)
    temp_path = f'data/raw/{file.filename}'
    with open(temp_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process pages one by one to save RAM
    total_chunks = 0
    with pdfplumber.open(temp_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_num = i + 1
            chunks = parser.parse_page(pdf, page, page_num, file.filename)
            if chunks:
                store.add(chunks)
                total_chunks += len(chunks)
                
    return {'status': 'success', 'chunks_added': total_chunks}

@router.post('/query', response_model=QueryResponse)
async def query(request: QueryRequest):
    results = store.search(request.query, k=request.k)
    context_text = '\n'.join([res['content'] for res in results])
    
    prompt = f"Context information is below:\n{context_text}\n\nBased on this context, answer the query: {request.query}"
    answer = llm.generate(prompt)
    
    citations = [Citation(**res['metadata']) for res in results]
    return {'answer': answer, 'citations': citations}
