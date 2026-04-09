# NomadIQ

NomadIQ is a mobile application designed to help people discover places based on their experience level in a city or country.

## Idea

Most travel apps show the same popular places to everyone. This works well for tourists who visit a place for the first time, but it becomes less useful for people who already know the city.

NomadIQ solves this problem by adapting recommendations depending on the user.

- First-time visitors see well-known landmarks and must-see places  
- Advanced users get recommendations for less popular, local spots  

## Problem

- Beginners often feel overwhelmed by too many options  
- Experienced users get bored of seeing the same popular places  
- Existing apps don’t adjust content based on user experience  

## Solution

The app introduces an **experience-based filtering system**:

- **First-Timer mode** → popular and highly rated places  
- **Advanced mode** → hidden gems and local spots  

Users can switch between modes anytime.

## Main Features

- Experience toggle (First-Timer / Advanced)
- Map with locations (Mapbox)
- Filters by category (food, nature, student-friendly, etc.)
- Visited places tracking
- Personalized recommendations

## How It Works

1. User opens the app and allows location access  
2. Selects experience level  
3. Sees places on the map  
4. Opens place details  
5. Marks places as visited  

The app then updates future recommendations based on user activity.

## Technology Stack

- **Mobile**: Android (Java, XML)
- **Backend**: Python (FastAPI)
- **Database**: PostgreSQL
- **APIs**: Google Places API, Mapbox

## Data Approach

We use a hybrid approach:
- Initial data is fetched from Google Places API  
- Then stored in our database  
- All filtering and recommendations work locally  

This improves performance and reduces API usage.

## Expected Result

A working prototype where users can:
- Search and filter places  
- Switch between experience modes  
- Get personalized suggestions  
- Track visited locations  

## Future Improvements

- More advanced recommendation system  
- User preferences (budget, interests)  
- Social features (reviews, sharing)  
- Multi-city support  

## Team

NomadIQ Project Team
