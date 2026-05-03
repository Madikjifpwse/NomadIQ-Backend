# NomadIQ — Smart City Guide

Backend for **NomadIQ** — a mobile app that helps users find places in Almaty based on their experience level (first-time visitors or advanced users).

### **2. Topic Area**
* Travel Technology and Tourism
* Personalized Recommendation Systems

### **3. Problem Statement**
* **What gap exists:** Standard travel apps offer a "one-size-fits-all" approach, providing the same recommendations regardless of a user's familiarity with a city[cite: 1].
* **Who is affected:** Both first-time tourists who feel overwhelmed by unstructured choices, and experienced travelers who are frustrated by generic recomendations.
* **Why this problem matters:** Without personalized discovery tools, travelers waste time planning, miss out on the specific emotions or experiences they are seeking, and fail to connect deeply with their destination.

### **4. Proposed Solution**
* We propose a dynamic, personalized travel mobile app that adapts its recommendations based on the user's experience level with a given destination. 
* For first-timers, the app curates optimized routes to popular, "must-see" landmarks to guarantee a high-quality introductory experience[cite: 1]. 
* For returning or experienced travelers, the system shifts focus, bypassing generic hotspots to recommend hidden gems, local favorites, and unique activities designed to evoke new emotions and deeper cultural immersion.

### **5. Target Users**
* **Novice/First-Time Tourists:** Users looking for reliable, easy-to-navigate guides to a city's most famous attractions.
* **Seasoned/Returning Travelers:** Users seeking novelty, off-the-beaten-path locations, and authentic local experiences.

How do these align with your vision for the app, or would you like to start brainstorming the Tech Stack and Key Features next?

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
* madikhan madiyar - back-end developer [230103114]
* imangali myngzhassar - front-end developer 230103061
* adil izbassar project manager 230103070
