from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Place, PlaceTag, User, ExperienceLevel
from app.utils.security import hash_password
import uuid


def create_sample_users(db: Session):
    print("Cleaning and creating users...")
    db.query(User).delete()

    users = [
        {
            "username": "alice_first_timer",
            "email": "alice@example.com",
            "password_hash": hash_password("password123"),
            "experience_level": ExperienceLevel.FIRST_TIMER
        },
        {
            "username": "bob_advanced",
            "email": "bob@example.com",
            "password_hash": hash_password("password123"),
            "experience_level": ExperienceLevel.ADVANCED
        }
    ]

    for user_data in users:
        user = User(**user_data)
        db.add(user)

    db.commit()
    print(f"Created {len(users)} sample users")


def create_sample_places(db: Session):
    print("Cleaning and creating 40 sample places...")
    # Очистка старых данных (важно для связей)
    db.query(PlaceTag).delete()
    db.query(Place).delete()
    db.commit()

    places_data = [
        # --- MUST SEE (1-10) ---
        {"name": "Shymbulak Mountain Resort",
         "description": "High-altitude ski resort with breathtaking views of the Zailiyskiy Alatau.",
         "category": "must_see", "latitude": 43.1285, "longitude": 77.0805, "address": "Gornaya St 640",
         "popularity_score": 98, "tags": ["mountains", "sports", "views"],
         "image_url": "https://images.unsplash.com/photo-1544112108-7a5611094034?q=80&w=600"},
        {"name": "Medeu Skating Rink", "description": "World's highest outdoor speed skating rink.",
         "category": "must_see", "latitude": 43.1574, "longitude": 77.0591, "address": "Gornaya St 465",
         "popularity_score": 95, "tags": ["ice", "sports", "historic"],
         "image_url": "https://images.unsplash.com/photo-1517176118179-65244ad0e60a?q=80&w=600"},
        {"name": "Ascension Cathedral", "description": "A unique wooden Russian Orthodox cathedral in Panfilov Park.",
         "category": "must_see", "latitude": 43.2594, "longitude": 76.9531, "address": "Gogol St 40",
         "popularity_score": 92, "tags": ["culture", "historic", "architecture"],
         "image_url": "https://images.unsplash.com/photo-1590333746438-281fd6f963d6?q=80&w=600"},
        {"name": "Kok Tobe Hill", "description": "A hill with a panoramic view of Almaty, reachable by cable car.",
         "category": "must_see", "latitude": 43.2323, "longitude": 76.9758, "address": "Dostyk Ave 104B",
         "popularity_score": 94, "tags": ["views", "family", "sunset"],
         "image_url": "https://images.unsplash.com/photo-1629813330971-85e83ecf0393?q=80&w=600"},
        {"name": "Big Almaty Lake", "description": "Alpine reservoir with stunning turquoise water.",
         "category": "must_see", "latitude": 43.0506, "longitude": 76.9845, "address": "Ili-Alatau National Park",
         "popularity_score": 100, "tags": ["nature", "lake", "hiking"],
         "image_url": "https://images.unsplash.com/photo-1589146142750-653a94833291?q=80&w=600"},
        {"name": "Central State Museum", "description": "Kazakhstan's largest museum showcasing history and culture.",
         "category": "must_see", "latitude": 43.2361, "longitude": 76.9511, "address": "Samal-1, 44",
         "popularity_score": 75, "tags": ["museum", "history", "education"],
         "image_url": "https://images.unsplash.com/photo-1566127444979-b3d2b654e3d7?q=80&w=600"},
        {"name": "Green Bazaar", "description": "Traditional market offering fresh produce and local delicacies.",
         "category": "must_see", "latitude": 43.2642, "longitude": 76.9545, "address": "Zenkov St 53",
         "popularity_score": 80, "tags": ["food", "local", "shopping"],
         "image_url": "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?q=80&w=600"},
        {"name": "Arbat Pedestrian Street", "description": "Main walking street with street artists and cozy cafes.",
         "category": "must_see", "latitude": 43.2621, "longitude": 76.9423, "address": "Zhibek Zholy Ave",
         "popularity_score": 88, "tags": ["walking", "art", "social"],
         "image_url": "https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?q=80&w=600"},
        {"name": "First President's Park", "description": "Huge urban park with a monumental fountain.",
         "category": "must_see", "latitude": 43.1895, "longitude": 76.8839, "address": "Dulatova St",
         "popularity_score": 85, "tags": ["park", "free", "nature"],
         "image_url": "https://images.unsplash.com/photo-1588714477688-cf28a50e94f7?q=80&w=600"},
        {"name": "Almaty Opera House", "description": "Beautiful architectural landmark for ballet and opera.",
         "category": "must_see", "latitude": 43.2494, "longitude": 76.9451, "address": "Kabanbai Batyr St 110",
         "popularity_score": 82, "tags": ["culture", "theatre", "architecture"],
         "image_url": "https://images.unsplash.com/photo-1503923352236-092556910609?q=80&w=600"},

        # --- STUDENT FRIENDLY (11-20) ---
        {"name": "National Library", "description": "Quiet place for study with free Wi-Fi.",
         "category": "student_friendly", "latitude": 43.2398, "longitude": 76.9455, "address": "Abay Ave 14",
         "popularity_score": 70, "tags": ["study", "quiet", "free"],
         "image_url": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?q=80&w=600"},
        {"name": "Coffee Boom Satpayev", "description": "Great Wi-Fi and student atmosphere.",
         "category": "student_friendly", "latitude": 43.2378, "longitude": 76.9354, "address": "Satpayev St 7",
         "popularity_score": 88, "tags": ["wifi", "coffee", "study"],
         "image_url": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?q=80&w=600"},
        {"name": "Dodo Pizza Arbat", "description": "Affordable and social pizza spot.", "category": "student_friendly",
         "latitude": 43.2625, "longitude": 76.9415, "address": "Kunaev St 41", "popularity_score": 85,
         "tags": ["food", "budget", "social"],
         "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=600"},
        {"name": "Satpayev University Park", "description": "Small park to rest between lectures.",
         "category": "student_friendly", "latitude": 43.2365, "longitude": 76.9312, "address": "Satpayev St 22",
         "popularity_score": 60, "tags": ["park", "free", "students"],
         "image_url": "https://images.unsplash.com/photo-1566433316213-3be05ccc02c1?q=80&w=600"},
        {"name": "Bowler Coffee", "description": "Specialty coffee with student discounts.",
         "category": "student_friendly", "latitude": 43.2522, "longitude": 76.9451, "address": "Kabanbai Batyr 65",
         "popularity_score": 78, "tags": ["coffee", "discount", "urban"],
         "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?q=80&w=600"},
        {"name": "Esentai River Path", "description": "Perfect for jogging or walking with earphones.",
         "category": "student_friendly", "latitude": 43.2205, "longitude": 76.9285, "address": "Esentai Bank",
         "popularity_score": 65, "tags": ["walking", "nature", "free"],
         "image_url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=600"},
        {"name": "Vanilla Cafe", "description": "Famous cheap buns and tea.", "category": "student_friendly",
         "latitude": 43.2415, "longitude": 76.9482, "address": "Kunaev St 130", "popularity_score": 90,
         "tags": ["food", "budget", "bakery"],
         "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=600"},
        {"name": "Dostyk Plaza Cinema", "description": "Standard hangout for movie nights.",
         "category": "student_friendly", "latitude": 43.2335, "longitude": 76.9575, "address": "Samal-2",
         "popularity_score": 80, "tags": ["movies", "shopping", "leisure"],
         "image_url": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=600"},
        {"name": "Atakent Exhibition Center", "description": "Vibrant park area with fountains and statues.",
         "category": "student_friendly", "latitude": 43.2235, "longitude": 76.9085, "address": "Timiryazev St",
         "popularity_score": 75, "tags": ["park", "free", "photo"],
         "image_url": "https://images.unsplash.com/photo-1596464716127-f2a82984de30?q=80&w=600"},
        {"name": "Mega Center Foodcourt", "description": "Wide selection of fast food for groups.",
         "category": "student_friendly", "latitude": 43.2012, "longitude": 76.8915, "address": "Rozybakiev St",
         "popularity_score": 82, "tags": ["food", "social", "shopping"],
         "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=600"},

        # --- LOCAL SECRETS (21-30) ---
        {"name": "Dom 36 Baribayeva", "description": "Art community and creative space in an old house.",
         "category": "local_secret", "latitude": 43.2589, "longitude": 76.9621, "address": "Baribayeva 36",
         "popularity_score": 35, "tags": ["art", "underground", "community"],
         "image_url": "https://images.unsplash.com/photo-1460661419201-fd4cecea8f82?q=80&w=600"},
        {"name": "Arasan Wellness", "description": "Historic Soviet-era bathhouse experience.",
         "category": "local_secret", "latitude": 43.2567, "longitude": 76.9286, "address": "Tole Bi St",
         "popularity_score": 40, "tags": ["wellness", "historic", "relax"],
         "image_url": "https://images.unsplash.com/photo-1544161515-4ae6ce6ca606?q=80&w=600"},
        {"name": "Nedelka Square", "description": "Quiet square with fountains behind the opera house.",
         "category": "local_secret", "latitude": 43.2486, "longitude": 76.9458, "address": "Baiseitova St",
         "popularity_score": 45, "tags": ["quiet", "vintage", "urban"],
         "image_url": "https://images.unsplash.com/photo-1572085312061-05df14bc9724?q=80&w=600"},
        {"name": "Botanical Garden", "description": "Lush forest-like garden away from city noise.",
         "category": "local_secret", "latitude": 43.2194, "longitude": 76.9175, "address": "Timiryazev St 36",
         "popularity_score": 55, "tags": ["nature", "quiet", "relax"],
         "image_url": "https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?q=80&w=600"},
        {"name": "Kasteyev Arts Museum", "description": "Finest art collection in Kazakhstan.",
         "category": "local_secret", "latitude": 43.2355, "longitude": 76.9189, "address": "Satpayev 30A",
         "popularity_score": 30, "tags": ["art", "museum", "culture"],
         "image_url": "https://images.unsplash.com/photo-1518998053901-5348d3961a04?q=80&w=600"},
        {"name": "Terrenkur Path", "description": "The Health Path along the river.", "category": "local_secret",
         "latitude": 43.2255, "longitude": 76.9654, "address": "Tatibekova St", "popularity_score": 50,
         "tags": ["walking", "health", "locals"],
         "image_url": "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=80&w=600"},
        {"name": "Aura Cafe Garden", "description": "Hidden backyard cafe with trees.", "category": "local_secret",
         "latitude": 43.2441, "longitude": 76.9421, "address": "Kurmangazy St", "popularity_score": 25,
         "tags": ["cafe", "hidden", "romantic"],
         "image_url": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?q=80&w=600"},
        {"name": "Tselinny Center", "description": "Modern art in a repurposed Soviet cinema.",
         "category": "local_secret", "latitude": 43.2422, "longitude": 76.9312, "address": "Masanchi 59",
         "popularity_score": 20, "tags": ["art", "cinema", "modern"],
         "image_url": "https://images.unsplash.com/photo-1499781350541-7783f6c6a0c8?q=80&w=600"},
        {"name": "Rakhat Shop", "description": "Smell of chocolate from the factory shop.", "category": "local_secret",
         "latitude": 43.2645, "longitude": 76.9430, "address": "Zenkov St", "popularity_score": 60,
         "tags": ["food", "local", "sweets"],
         "image_url": "https://images.unsplash.com/photo-1549007994-cb92ca71450a?q=80&w=600"},
        {"name": "Small Almaty Bridge", "description": "Secret bridge with amazing sunset view.",
         "category": "local_secret", "latitude": 43.2381, "longitude": 76.9612, "address": "Samal Path",
         "popularity_score": 15, "tags": ["secret", "sunset", "view"],
         "image_url": "https://images.unsplash.com/photo-1449034446853-66c86144b0ad?q=80&w=600"},

        # --- OTHER (31-40) ---
        {"name": "Esentai Mall", "description": "Luxury shopping center.", "category": "other", "latitude": 43.2185,
         "longitude": 76.9285, "address": "Al-Farabi 77", "popularity_score": 85, "tags": ["luxury", "shopping"],
         "image_url": "https://images.unsplash.com/photo-1567449303078-57ad995bd301?q=80&w=600"},
        {"name": "Republican Palace", "description": "Grand concert hall area.", "category": "other",
         "latitude": 43.2435, "longitude": 76.9585, "address": "Dostyk 56", "popularity_score": 70,
         "tags": ["concert", "square"],
         "image_url": "https://images.unsplash.com/photo-1514306191717-452ec28c7814?q=80&w=600"},
        {"name": "Auezov Theater", "description": "Kazakh drama theater building.", "category": "other",
         "latitude": 43.2411, "longitude": 76.9185, "address": "Abay 103", "popularity_score": 65,
         "tags": ["theatre", "culture"],
         "image_url": "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?q=80&w=600"},
        {"name": "Circus Almaty", "description": "Unique UFO-shaped building.", "category": "other",
         "latitude": 43.2392, "longitude": 76.9165, "address": "Abay 50", "popularity_score": 60,
         "tags": ["circus", "architecture"],
         "image_url": "https://images.unsplash.com/photo-1502635385003-ee1e6a1a742d?q=80&w=600"},
        {"name": "St. Nicholas Cathedral", "description": "Historic blue-domed church.", "category": "other",
         "latitude": 43.2505, "longitude": 76.9295, "address": "Baytursynov St", "popularity_score": 55,
         "tags": ["historic", "church"],
         "image_url": "https://images.unsplash.com/photo-1548703353-d74236077543?q=80&w=600"},
        {"name": "Military History Museum", "description": "Outdoor tank and plane exhibit.", "category": "other",
         "latitude": 43.2575, "longitude": 76.9525, "address": "Zenkov 24", "popularity_score": 45,
         "tags": ["museum", "military"],
         "image_url": "https://images.unsplash.com/photo-1580136608260-4cd11f4c244e?q=80&w=600"},
        {"name": "Central Park Almaty", "description": "Classic amusement park with a lake.", "category": "other",
         "latitude": 43.2625, "longitude": 76.9725, "address": "Gogol 1", "popularity_score": 78,
         "tags": ["park", "fun", "family"],
         "image_url": "https://images.unsplash.com/photo-1533107862482-0e6974b06ec4?q=80&w=600"},
        {"name": "Sky Bar Ritz", "description": "Posh bar with Al-Farabi view.", "category": "other",
         "latitude": 43.2191, "longitude": 76.9281, "address": "Al-Farabi 77/7", "popularity_score": 40,
         "tags": ["premium", "view", "nightlife"],
         "image_url": "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?q=80&w=600"},
        {"name": "Kabanbai Batyr Food", "description": "A street with many fast food options.", "category": "other",
         "latitude": 43.2501, "longitude": 76.9433, "address": "Kabanbai Batyr", "popularity_score": 68,
         "tags": ["food", "street"],
         "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?q=80&w=600"},
        {"name": "Nikolskiy Market", "description": "Authentic local small market.", "category": "other",
         "latitude": 43.2515, "longitude": 76.9290, "address": "Baytursynov", "popularity_score": 35,
         "tags": ["local", "market", "traditional"],
         "image_url": "https://images.unsplash.com/photo-1488459716781-31db52582fe9?q=80&w=600"}
    ]

    created_count = 0
    for place_data in places_data:
        tags = place_data.pop("tags", [])
        place = Place(**place_data)
        db.add(place)
        db.flush()  # Получаем ID места

        for tag in tags:
            place_tag = PlaceTag(place_id=place.id, tag=tag)
            db.add(place_tag)
        created_count += 1

    db.commit()
    print(f"✓ Created {created_count} sample places with tags and images!")


def seed_database():
    print("\n" + "=" * 50)
    print("NomadIQ Database Seeder (FINAL MVP)")
    print("=" * 50 + "\n")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        create_sample_users(db)
        create_sample_places(db)
        print("\n" + "=" * 50)
        print("SEEDING COMPLETED SUCCESSFULLY!")
        print("=" * 50)
    except Exception as e:
        print(f"\nError seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()