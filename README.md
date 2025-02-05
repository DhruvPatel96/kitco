# Kitco AI Content Gateway

This repository contains a **full-stack** application enabling multiple **Kitco News** teams—Editorial, Video, Anchors, Marketing, and Social Media—to rapidly generate AI-driven, context-rich content. The project is split into two main parts:

1. **BackEnd**: A FastAPI-based microservice system for content generation, news retrieval (FAISS index), feedback loops, and more.  
2. **FrontEnd**: A Next.js client that allows users to interact with these microservices, generate content, and provide feedback in real time.

Below is an overview of the repository structure, along with instructions on how to set up, run, and contribute to the project.

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Key Features](#key-features)  
3. [Repository Structure](#repository-structure)  
   - [BackEnd](#backend-folder-structure)  
   - [FrontEnd](#frontend-folder-structure)  
4. [Tech Stack](#tech-stack)  
5. [Setup & Installation](#setup--installation)  
   - [Local Environment](#local-environment)  
   - [Docker & Docker Compose](#docker--docker-compose)  
6. [Usage](#usage)  
7. [Environment Variables](#environment-variables)  
8. [Testing](#testing)  
9. [Contributing](#contributing)  
10. [License](#license)

---

## 1. Project Overview

**Kitco AI Content Gateway** provides real-time AI-driven content creation services for:

- **Editorial**: AP-style articles  
- **Video Production**: Video scripts and metadata (titles, descriptions, tags)  
- **Anchors**: Teleprompter scripts  
- **Marketing**: Real-time campaign ideas and analytics  
- **Social Media**: Platform-specific posts (e.g., Twitter, LinkedIn)

The system integrates:

- A **FastAPI** backend with modular routers for each team.  
- A **Next.js** frontend enabling easy interaction with the AI microservices and feedback loops.  
- A **MongoDB** database for storing articles, API keys, and user feedback.  
- A **FAISS** index for contextual retrieval of recent news articles (improving LLM outputs).

---

## 2. Key Features

- **Retrieval-Augmented Generation (RAG)**  
  Pulls recent news articles from MongoDB, uses **FAISS** to find relevant context, and provides more accurate AI outputs.

- **Microservice Architecture**  
  Each content endpoint (editorial, video, anchors, marketing, social) has its own route and prompt logic.

- **Feedback & Regeneration**  
  Users can mark outputs as *good* or *bad*; if *bad*, the system regenerates content using additional user instructions.

- **Full-Stack Setup**  
  Docker Compose orchestration for easy local or server-based deployment.

---


### BackEnd Folder Structure

- **Dockerfile**: Builds the FastAPI backend container.  
- **docker-compose.yml** (within `BackEnd`): An optional compose file specific to the backend.  
- **requirements.txt**: Python dependencies for FastAPI, Transformers, FAISS, etc.  
- **app/**  
  - **main.py**: Entry point for the FastAPI application.  
  - **config.py**: Reads environment variables, sets up configuration via Pydantic.  
  - **api_key_manager.py**: API key generation and validation logic.  
  - **faiss_index.index**: FAISS index file (binary) for quick retrieval.  
  - **models/**  
    - **faiss_indexer.py**: Utilities for building and saving FAISS indices.  
    - **llm_loader.py**: Loads and caches the language model (Hugging Face).  
    - **prompt_engineer.py**: Prompt templates for editorial, video, marketing, etc.  
    - **retrieval.py**: Retrieves relevant articles from FAISS for context-based generation.  
  - **routers/**  
    - **editorial.py**, **video.py**, **anchors.py**, **marketing.py**, **social.py**: Specialized endpoints for each team’s content generation.  
    - **feedback.py**: Endpoint to submit feedback and optionally trigger content regeneration.  
  - **services/**  
    - **news_fetcher.py**: Pulls articles from NewsAPI.org, stores them in MongoDB.  
    - **post_processor.py**: Functions for cleaning and formatting generated text.  
    - **regeneration.py**: Logic to regenerate content based on user feedback.  
  - **tests/**  
    - **test_endpoints.py**: Basic FastAPI integration tests.  
  - **utils/**  
    - **security.py**: Additional security layers, e.g., `api_key_dependency`.

### FrontEnd Folder Structure

- **Dockerfile**: Builds the Next.js frontend container.  
- **README.md** (within `FrontEnd`): Possibly a focused guide for the front-end.  
- **package.json**: Lists Node.js dependencies (React, Next.js, Tailwind, etc.).  
- **app/**  
  - **layout.tsx** & **page.tsx**: The main layout and home page for content generation UI.  
  - **globals.css**: Tailwind / general CSS.  
- **public/**: Static assets (svgs, icons, etc.).  
- **tsconfig.json**: TypeScript configuration.  
- **eslint.config.mjs**, **postcss.config.mjs**, **tailwind.config.ts**: Front-end configuration files.

---

## 3. Tech Stack

- **Backend**  
  - [FastAPI](https://fastapi.tiangolo.com/)  
  - [Transformers (Hugging Face)](https://github.com/huggingface/transformers)  
  - [Sentence Transformers](https://www.sbert.net/) + [FAISS](https://github.com/facebookresearch/faiss)  
  - [MongoDB](https://www.mongodb.com/)  

- **Frontend**  
  - [Next.js](https://nextjs.org/)  
  - [React](https://reactjs.org/)  
  - [Tailwind CSS](https://tailwindcss.com/)  

- **Containerization**  
  - [Docker](https://www.docker.com/) + [Docker Compose](https://docs.docker.com/compose/)

---

## 4. Setup & Installation

### Local Environment

1. **Clone** the repository:

   ```bash
   git clone https://github.com/yourusername/kitco-ai-content-gateway.git
   cd kitco-ai-content-gateway
