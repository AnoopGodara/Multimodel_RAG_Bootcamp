from pydantic import BaseModel
from typing import List, Optional, Dict

class QueryRequest(BaseModel):
    query: str
    k: Optional[int] = 4

class Citation(BaseModel):
    source: str
    page: int
    type: str

class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]

class IngestResponse(BaseModel):
    status: str
    chunks_added: int

class HealthStatus(BaseModel):
    status: str
    resources: Dict
    index_size: int

class ConfigResponse(BaseModel):
    model_name: str
    embedding_model: str
    vector_store: str
    version: str

