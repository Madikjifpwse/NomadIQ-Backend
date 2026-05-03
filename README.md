# NomadIQ Backend

Backend for NomadIQ — a mobile app that helps users find places based on their experience level (first-time visitors or advanced users).

## Features

- FastAPI + PostgreSQL
- JWT authentication
- Filter places (popular vs hidden spots)
- Tags and categories
- Location-based search
- Visited places tracking
- Simple recommendations

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