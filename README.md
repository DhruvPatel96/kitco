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

## 3. Repository Structure

Below is an abbreviated view of the file tree (refer to `full_project_dir_tree.txt` for a comprehensive listing):
.
├── BackEnd
│   ├── BE_Dir_Tree.txt
│   ├── Dockerfile
│   ├── app
│   │   ├── api_key_manager.py
│   │   ├── config.py
│   │   ├── faiss_index.index
│   │   ├── main.py
│   │   ├── models
│   │   │   ├── faiss_indexer.py
│   │   │   ├── llm_loader.py
│   │   │   ├── prompt_engineer.py
│   │   │   └── retrieval.py
│   │   ├── routers
│   │   │   ├── anchors.py
│   │   │   ├── editorial.py
│   │   │   ├── feedback.py
│   │   │   ├── marketing.py
│   │   │   ├── social.py
│   │   │   └── video.py
│   │   ├── services
│   │   │   ├── news_fetcher.py
│   │   │   ├── post_processor.py
│   │   │   └── regeneration.py
│   │   ├── tests
│   │   │   └── test_endpoints.py
│   │   └── utils
│   │       └── security.py
│   ├── docker-compose.yml
│   └── requirements.txt
├── FrontEnd
│   ├── Dockerfile
│   ├── FE_Dir_Tree.txt
│   ├── README.md
│   ├── app
│   │   ├── favicon.ico
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── eslint.config.mjs
│   ├── next-env.d.ts
│   ├── next.config.ts
│   ├── package.json
│   ├── postcss.config.mjs
│   ├── public
│   │   ├── file.svg
│   │   ├── globe.svg
│   │   ├── next.svg
│   │   ├── vercel.svg
│   │   └── window.svg
│   ├── tailwind.config.ts
│   └── tsconfig.json
├── README.md
├── docker-compose.yml
└── full_project_dir_tree.txt

11 directories, 45 files

