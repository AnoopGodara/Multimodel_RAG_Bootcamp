# Assignment Overview: Multimodal RAG System with FastAPI

## 1. Objective
Design, build, and deploy an end-to-end **Multimodal Retrieval-Augmented Generation (RAG)** system that solves a real-world problem in a specific professional or academic domain.

## 2. Core Requirements
### 2.1 Problem Statement (Graded)
*   **Location:** `README.md` under "Problem Statement" section.
*   **Length:** 500 - 800 words.
*   **Content:**
    *   Domain Identification (e.g., Healthcare, Legal, Finance).
    *   Specific problem description involving multimodal documents (text, tables, images).
    *   Uniqueness of the problem (domain-specific challenges).
    *   Justification for using RAG over other methods.
    *   Expected outcomes and supported queries.

### 2.2 Technical Capabilities
*   **Ingestion:** Process multimodal PDFs (Text, Tables, Images).
*   **Indexing:** Build a searchable vector index with metadata tracking.
*   **Retrieval:** Retrieve relevant context (text chunks, table data, image summaries).
*   **Generation:** Produce grounded answers using a Multimodal LLM (VLM).
*   **Citations:** Provide references back to the source document/page.

### 2.3 Required FastAPI Endpoints
*   `GET /health`: System status, uptime, and index stats (e.g., document count).
*   `POST /ingest`: Upload and process a multimodal PDF.
*   `POST /query`: Submit a natural language query and receive a grounded answer with citations.
*   `GET /config`: Return current system configuration (models used, version, etc.).

### 2.4 Sample Domain PDF
*   Must include at least one PDF from the chosen domain.
*   Must contain: Text, at least one Table, and at least one Image/Chart.

## 3. Repository Structure (Minimum)
```text
your-repo-name/
├── README.md                  # Problem statement, arch diagram, tech choices, setup
├── requirements.txt           # Pinned Python dependencies
├── .env.example               # Template for API keys
├── main.py                    # FastAPI application entry point
├── src/                       # Source code (modular)
│   ├── ingestion/             # Parsing, chunking, embedding
│   ├── retrieval/             # Vector store, query logic
│   ├── models/                # LLM/VLM wrappers
│   └── api/                   # FastAPI routes
├── sample_documents/          # Domain-specific multimodal PDF
├── screenshots/               # Evidence of working system
└── .gitignore                 # Excludes sensitive/unnecessary files
```

## 4. Deliverables in README.md
*   **Problem Statement** (500-800 words).
*   **Architecture Overview** (Diagram using Image or Mermaid).
*   **Technology Choices** (Justification for Parser, Embedding, Vector Store, LLM, VLM).
*   **Setup Instructions** (Step-by-step).
*   **API Documentation** (Sample request/response).
*   **Screenshots** (Swagger UI, Ingestion, Text/Table/Image queries, Health endpoint).
*   **Limitations & Future Work**.

## 5. Evaluation Criteria
*   **Problem Formulation (10%)**: Quality and relevance of the problem statement.
*   **System Architecture (20%)**: Modularity and appropriate technology choices.
*   **RAG Accuracy (30%)**: Tested by the evaluator with sample and unseen PDFs.
*   **Code Quality (15%)**: Clean, modular, and well-documented code.
*   **API Design (15%)**: Proper use of FastAPI, Pydantic models, and error handling.
*   **Robustness & Reproducibility (10%)**: Screenshots and clear setup instructions.

## 6. Submission Guidelines
*   **Format:** Public GitHub Repository URL.
*   **Deadline:** 14 calendar days from issue date.
*   **Integrity:** Original work only. Similarity detection and AI-generation checks will be performed. Incremental commit history is expected.

## 7. Tips for Success
1.  **Start with the Problem Statement** before coding.
2.  **Prototype first**, then refine.
3.  **Modularize code** (Inference, Retrieval, API layers).
4.  **Use Pydantic** for API contracts.
5.  **Test thoroughly** with multimodal queries.
6.  **Maintain a meaningful commit history**.
