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

### Features

- JWT-based user registration and login
- Role-based authorization for customers and admins
- Public product browsing and search
- Admin product and category management
- Customer cart and checkout workflows
- Customer order history and order details
- Admin access to all orders
- Centralized exception handling
- File and console logging
- Background order-confirmation task
- Router-level tests using pytest
---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Framework | Python FastAPI |
| Language | Python 3.12 |
| ORM | SQLAlchemy |
| Database | PostgreSQL / SQLite (local) |
| Validation | Pydantic |
| API Docs | Swagger |
| IDE | Visual Studio Code |

---
Method Endpoint Access

POST
/api/users/register
Public


POST
/api/users/login
Public


GET
/api/products/
Public


GET
/api/products/search
Public


POST
/api/admin/products/
Admin


PATCH
/api/admin/products/{id}/quantity
Admin


DELETE
/api/admin/products/{id}
Admin


GET
/api/categories/list
Public


POST
/api/admin/categories/
Admin


PATCH
/api/admin/categories/{id}
Admin


POST
/api/cart/
Authenticated user


PATCH
/api/cart/{id}
Cart owner


DELETE
/api/cart/{id}
Cart owner


POST
/api/orders/
Authenticated user


GET
/api/orders/history/{user_id}
Order owner


GET
/api/admin/orders
Admin

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

# 4. Start the application
uvicorn app.main:app --reload

