# NomadIQ — Smart City Guide

Backend for **NomadIQ** — a mobile app that helps users find places in Almaty based on their experience level (first-time visitors or advanced users).

## Features

- **FastAPI + Neon (PostgreSQL)**: High-performance asynchronous API with serverless cloud database.
- **JWT Authentication**: Secure user registration and login system.
- **Smart Filtering**: Categorize places by type (Cafe, Park, Museum) and experience level (Popular vs Hidden spots).
- **Visited Places Tracking**: Personal user history for explored locations.
- **Image Integration**: Optimized for Glide image loading on the frontend.
- **Database Migrations**: Managed via Alembic for easy schema updates.

## Tech Stack

- **Framework**: FastAPI
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Security**: JWT (Python-jose)

## Setup

### 1. Install

```bash
cd nomadiq-backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Team Members (Student IDs)
* 230103114
* 230103061
* 230103070
