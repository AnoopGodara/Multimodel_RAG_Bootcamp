# Automotive Ergonomics Multimodal RAG System

## Problem Statement
In the field of automotive engineering, designers face a significant challenge in cross-referencing information distributed across multimodal technical documents. Standard vehicle design catalogs contain intricate technical drawings, measurement tables, and detailed safety regulation text. Extracting actionable insights currently requires tedious manual search across these disparate modalities, leading to potential design errors or non-compliance with international safety standards.

This project implements a Multimodal Retrieval-Augmented Generation (RAG) system specifically tailored for Automotive Design. It enables engineers to query complex ergonomic data using natural language, retrieving and synthesizing information from text, tables, and interior diagrams simultaneously.

## Architecture
1. Ingestion: pdfplumber + Gemini API (summaries).
2. Indexing: all-MiniLM-L6-v2 + FAISS.
3. Inference: Qwen2.5-0.5B-Instruct (Local).
4. API: FastAPI.

## Technology Choices
- Parser: pdfplumber chosen for table structure retention.
- LLM: Qwen2.5-0.5B-Instruct for high performance in 8GB RAM.
- Vector Store: FAISS for speed and minimal overhead.

## Setup Instructions
1. Install: pip install -r requirements.txt
2. Configure: Add GEMINI_API_KEY to .env
3. Run: python main.py

## API Documentation
- `GET /`: Welcome message and documentation links.
- `GET /health`: Returns system health and resource status.
- `GET /config`: Returns system configuration.
- `POST /ingest`: Upload a PDF for ingestion.
- `POST /query`: Submit a query to the RAG system.

## Screenshots
Screenshots of Swagger UI, Ingestion, Text/Table/Image queries, Health endpoint are available in the `screenshots/` directory.

## Limitations & Future Work
- Currently relies on a single VLM API (Gemini).
- Local LLM inference speed can be improved with better hardware.
- Future work includes implementing a more complex re-ranking mechanism and supporting additional multimodal formats.
