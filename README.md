# ☕ KohiCebu FastAPI

A RESTful API developed for the **KohiCebu Digital Ordering and Management System** using FastAPI and Python.

This project demonstrates how a coffee shop information system can manage products, customers, and orders through a structured REST API.

---

## 📌 Project Overview

KohiCebu FastAPI provides API endpoints for managing:

- Products
- Customers
- Orders

The API includes CRUD operations, request validation, product availability checking, stock validation, and automatic order total calculation.

---

## 🛠️ Technologies Used

- **Python 3**
- **FastAPI**
- **Pydantic**
- **Uvicorn**
- **REST API**
- **Git & GitHub**

---

## 📂 Project Structure

```text
KohiCebu-FastAPI/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── database.py
│   │
│   ├── models/
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   └── __init__.py
│   │
│   └── routes/
│       ├── __init__.py
│       ├── products.py
│       ├── customers.py
│       └── orders.py
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── venv/