# filename: README.md

# Online Shopping Application – User Module

---

## Candidate Information

| Field | Details |
|---|---|
| **Name** | Amitanshu Pattnaik |
| **Email** | amitanshupattnaik@deloitte.com |
| **Assessment Batch** | FY27 - Python / 07-08-26 |

---

## Project Overview

ABC is expanding its successful physical store to an online platform.  
This project implements the **User Module** of an Online Shopping Application  
using **Python FastAPI** with a clean layered architecture.

### Key Features
- User Registration & Login
- Browse & Search Products by name and category
- Manage Shopping Cart (Add, Update, Remove, Summary)
- Place Orders & View Order History
- Dockerized setup with PostgreSQL

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Framework | Python FastAPI |
| Language | Python 3.12 |
| ORM | SQLAlchemy |
| Database | PostgreSQL (Docker) / SQLite (local) |
| Validation | Pydantic |
| API Docs | Swagger / OpenAPI |
| Containerization | Docker + Docker Compose |
| IDE | Visual Studio Code |

---

## Project Structure
app/
├── main.py
├── db/
│   ├── session.py
│   └── base.py
├── models/
│   ├── user.py
│   ├── category.py
│   ├── product.py
│   ├── cart.py
│   └── order.py
├── schemas/
│   ├── user_schema.py
│   ├── product_schema.py
│   ├── cart_schema.py
│   └── order_schema.py
├── repositories/
│   ├── user_repository.py
│   ├── product_repository.py
│   ├── cart_repository.py
│   └── order_repository.py
├── services/
│   ├── user_service.py
│   ├── product_service.py
│   ├── cart_service.py
│   └── order_service.py
├── routers/
│   ├── user_router.py
│   ├── product_router.py
│   ├── cart_router.py
│   └── order_router.py
└── utils/
├── exceptions.py
└── helpers.py

## Setup Instructions

### Option 1 — Run Locally

# 1. Clone the repository
git clone <repo-url>
cd <project-folder>

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure environment variables
cp .env.example .env
# Edit .env with your DB credentials

# 5. Start the application
uvicorn app.main:app --reload

