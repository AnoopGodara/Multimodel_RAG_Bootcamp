# Multimodal RAG Project Plan (1-Hour Sprint)

## 1. Objectives
    - Build a fully functional Multimodal RAG system for Automotive Ergonomics.
- Use a local LLM (Qwen2.5-0.5B) for answering queries.
- Use Gemini API only for image/table descriptions.
- Ensure 100% stability on 8GB RAM / 16GB Disk.

## 2. Tech Stack
- **API:** FastAPI
- **LLM:** Qwen2.5-0.5B-Instruct (Local)
- **Vector DB:** FAISS
- **Embeddings:** all-MiniLM-L6-v2 (Local)
- **Parsing:** pdfplumber + Gemini (for images)

## 3. Implementation Schedule
| Time | Phase | Focus |
| :--- | :--- | :--- |
| 00-05 | Setup | Requirements, Resource Guardrails, Project Structure |
| 05-15 | Models | Download/Cache Local LLM & Embeddings |
| 15-30 | Ingestion | Multimodal parsing (Text, Tables, Image Summaries) |
| 30-40 | Indexing | FAISS Indexing with Metadata |
| 40-55 | API | FastAPI Endpoints (/ingest, /query, /health) |
| 55-60 | Finalize | README, Problem Statement, Final Tests |

## 4. Resource Guardrails
- **RAM Check:** `psutil.virtual_memory()` monitoring.
- **Disk Check:** `shutil.disk_usage()` monitoring.
- **Optimization:** CPU-only torch, 4-bit quantization where possible, lazy loading.
