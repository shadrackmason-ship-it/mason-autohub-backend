"""
Seed demo data — runs once on startup when the database is empty.
Demo login: demo@masonautohub.com / demo1234
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.car import Car
from app.models.mechanic import Mechanic
from app.models.spare_part import SparePart
from app.models.user import User


def seed_demo_data(db: Session) -> None:
    # Only seed once
    if db.scalar(select(User).limit(1)):
        return

    # ── Demo user ─────────────────────────────────────────────────────────────
    demo = User(
        full_name="Mason AutoHub Demo",
        email="demo@masonautohub.com",
        password_hash=hash_password("demo1234"),
        role="dealer",
        phone="+254 700 000 000",
    )
    db.add(demo)
    db.flush()  # get demo.id

    # ── Cars ──────────────────────────────────────────────────────────────────
    cars = [
        Car(owner_id=demo.id, make="Toyota", model="Land Cruiser Prado",
            year=2021, price=5_200_000, mileage=35_000, fuel_type="Diesel",
            transmission="Automatic", engine_cc=2800, body_type="SUV",
            location="Nairobi", condition="used", is_featured=True,
            description="Clean verified local unit. Full service history, new tyres, bull bar fitted. Ready to drive.",
            image_url="https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?q=80&w=1200&auto=format&fit=crop"),

        Car(owner_id=demo.id, make="Mercedes-Benz", model="C300",
            year=2022, price=10_400_000, mileage=15_000, fuel_type="Petrol",
            transmission="Automatic", engine_cc=2000, body_type="Sedan",
            location="Nairobi", condition="used", is_featured=True,
            description="One owner, accident-free. Panoramic roof, AMG package, full dealer service history.",
            image_url="https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?q=80&w=1200&auto=format&fit=crop"),

        Car(owner_id=demo.id, make="BMW", model="X5 xDrive40i",
            year=2021, price=12_800_000, mileage=28_000, fuel_type="Petrol",
            transmission="Automatic", engine_cc=3000, body_type="SUV",
            location="Nairobi", condition="used", is_featured=True,
            description="M Sport package, 7-seat configuration, heads-up display, harman/kardon sound.",
            image_url="https://images.unsplash.com/photo-1555215695-3004980ad54e?q=80&w=1200&auto=format&fit=crop"),

        Car(owner_id=demo.id, make="Toyota", model="Hilux Double Cab",
            year=2023, price=6_500_000, mileage=8_000, fuel_type="Diesel",
            transmission="Manual", engine_cc=2800, body_type="Truck",
            location="Nairobi", condition="new", is_featured=True,
            description="Brand new 2023 Hilux. Locally assembled, full warranty, canopy included.",
            image_url="https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?q=80&w=1200&auto=format&fit=crop"),

        Car(owner_id=demo.id, make="Subaru", model="Forester XT",
            year=2020, price=3_450_000, mileage=52_000, fuel_type="Petrol",
            transmission="Automatic", engine_cc=2000, body_type="SUV",
            location="Mombasa", condition="used", is_import=True,
            description="Japan import, clean JAAI inspection report. Turbo engine, EyeSight safety system.",
            image_url="https://images.unsplash.com/photo-1568844293986-8d0400bd4745?q=80&w=1200&auto=format&fit=crop"),

        Car(owner_id=demo.id, make="Mazda", model="CX-5 Skyactiv",
            year=2021, price=4_100_000, mileage=41_000, fuel_type="Petrol",
            transmission="Automatic", engine_cc=2500, body_type="SUV",
            location="Nairobi", condition="used", is_import=True,
            description="UK import, full service history. Leather interior, BOSE sound, 360 camera.",
            image_url="https://images.unsplash.com/photo-1606016159991-dfe4f2746ad5?q=80&w=1200&auto=format&fit=crop"),

        Car(owner_id=demo.id, make="Porsche", model="911 Carrera S",
            year=2022, price=20_500_000, mileage=12_000, fuel_type="Petrol",
            transmission="Automatic", engine_cc=3000, body_type="Coupe",
            location="Nairobi", condition="used", is_featured=True,
            description="Iconic rear-engine sports car. Sport Chrono package, PASM, ceramic brakes.",
            image_url="https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=1200&auto=format&fit=crop"),

        Car(owner_id=demo.id, make="Land Rover", model="Range Rover Sport",
            year=2022, price=14_600_000, mileage=22_000, fuel_type="Diesel",
            transmission="Automatic", engine_cc=3000, body_type="SUV",
            location="Nairobi", condition="used", is_featured=True,
            description="HSE Dynamic spec. Meridian sound, air suspension, panoramic roof, tow pack.",
            image_url="https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?q=80&w=1200&auto=format&fit=crop"),

        Car(owner_id=demo.id, make="Volkswagen", model="Tiguan Allspace",
            year=2021, price=5_800_000, mileage=38_000, fuel_type="Petrol",
            transmission="Automatic", engine_cc=2000, body_type="SUV",
            location="Nairobi", condition="used", is_import=True,
            description="7-seater, panoramic roof, digital cockpit. Germany import, full VW service history.",
            image_url="https://images.unsplash.com/photo-1606016159991-dfe4f2746ad5?q=80&w=1200&auto=format&fit=crop"),

        Car(owner_id=demo.id, make="Toyota", model="Camry XSE",
            year=2022, price=4_900_000, mileage=19_000, fuel_type="Hybrid",
            transmission="Automatic", engine_cc=2500, body_type="Sedan",
            location="Kisumu", condition="used",
            description="Hybrid sedan, exceptional fuel economy. JBL sound, wireless charging, safety sense.",
            image_url="https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?q=80&w=1200&auto=format&fit=crop"),

        Car(owner_id=demo.id, make="Nissan", model="X-Trail",
            year=2020, price=3_200_000, mileage=61_000, fuel_type="Petrol",
            transmission="Automatic", engine_cc=2000, body_type="SUV",
            location="Nakuru", condition="used", is_import=True,
            description="Japan import, 7-seater, ProPilot assist. Clean JEVIC inspection, new timing chain.",
            image_url="https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?q=80&w=1200&auto=format&fit=crop"),

        Car(owner_id=demo.id, make="Honda", model="CR-V",
            year=2021, price=3_750_000, mileage=44_000, fuel_type="Petrol",
            transmission="Automatic", engine_cc=1500, body_type="SUV",
            location="Nairobi", condition="used", is_import=True,
            description="Turbocharged 1.5L, Honda Sensing suite, heated seats, Apple CarPlay.",
            image_url="https://images.unsplash.com/photo-1568844293986-8d0400bd4745?q=80&w=1200&auto=format&fit=crop"),
    ]
    db.add_all(cars)

    # ── Mechanics ─────────────────────────────────────────────────────────────
    mechanics = [
        Mechanic(name="Mason Auto Garage", location="Kitengela, Nairobi",
                 specialty="Engine Overhaul & Diagnostics", rating=4.9,
                 review_count=146, phone="+254 700 000 001", is_open=True),
        Mechanic(name="Westlands Auto Care", location="Westlands, Nairobi",
                 specialty="Full Service & Diagnostics", rating=4.7,
                 review_count=89, phone="+254 711 000 002", is_open=True),
        Mechanic(name="Karen Motors", location="Karen, Nairobi",
                 specialty="Electrical Systems & AC", rating=4.8,
                 review_count=201, phone="+254 722 000 003", is_open=True),
        Mechanic(name="Mombasa Road Garage", location="Mombasa Road, Nairobi",
                 specialty="Tires, Alignment & Suspension", rating=4.6,
                 review_count=134, phone="+254 733 000 004", is_open=True),
        Mechanic(name="Thika Road Auto Hub", location="Thika Road, Nairobi",
                 specialty="Bodywork & Painting", rating=4.5,
                 review_count=78, phone="+254 744 000 005", is_open=True),
        Mechanic(name="Kisumu Central Garage", location="Kisumu",
                 specialty="Diesel Engines & Gearboxes", rating=4.7,
                 review_count=112, phone="+254 755 000 006", is_open=True),
        Mechanic(name="Coast Auto Specialists", location="Mombasa",
                 specialty="Japanese Imports & Hybrid Systems", rating=4.8,
                 review_count=95, phone="+254 766 000 007", is_open=True),
        Mechanic(name="Nakuru Auto Works", location="Nakuru",
                 specialty="4WD & Off-Road Specialists", rating=4.6,
                 review_count=67, phone="+254 777 000 008", is_open=False),
    ]
    db.add_all(mechanics)

    # ── Spare parts ───────────────────────────────────────────────────────────
    parts = [
        SparePart(name="Toyota Genuine Oil Filter", brand="Toyota Genuine",
                  category="Filters", price=850, stock=42,
                  img="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=400&auto=format&fit=crop"),
        SparePart(name="K&N High-Flow Air Filter", brand="K&N",
                  category="Filters", price=4_200, stock=18,
                  img="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=400&auto=format&fit=crop"),
        SparePart(name="Bosch Cabin Air Filter", brand="Bosch",
                  category="Filters", price=1_400, stock=35,
                  img="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=400&auto=format&fit=crop"),
        SparePart(name="Brembo Front Brake Pads", brand="Brembo",
                  category="Brakes", price=6_500, stock=30,
                  img="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=400&auto=format&fit=crop"),
        SparePart(name="Bosch Rear Brake Disc", brand="Bosch",
                  category="Brakes", price=8_800, stock=12,
                  img="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=400&auto=format&fit=crop"),
        SparePart(name="EBC Brake Shoes — Rear", brand="EBC",
                  category="Brakes", price=3_200, stock=24,
                  img="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=400&auto=format&fit=crop"),
        SparePart(name="Exide 60Ah Car Battery", brand="Exide",
                  category="Batteries", price=12_000, stock=8,
                  img="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=400&auto=format&fit=crop"),
        SparePart(name="Amaron 55Ah MF Battery", brand="Amaron",
                  category="Batteries", price=10_500, stock=15,
                  img="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=400&auto=format&fit=crop"),
        SparePart(name="Philips H4 LED Headlight Bulb", brand="Philips",
                  category="Lighting", price=3_200, stock=55,
                  img="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=400&auto=format&fit=crop"),
        SparePart(name="Osram Night Breaker H7", brand="Osram",
                  category="Lighting", price=2_800, stock=40,
                  img="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=400&auto=format&fit=crop"),
        SparePart(name="KYB Front Shock Absorber", brand="KYB",
                  category="Suspension", price=8_500, stock=20,
                  img="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=400&auto=format&fit=crop"),
        SparePart(name="Monroe Rear Shock Absorber", brand="Monroe",
                  category="Suspension", price=7_200, stock=16,
                  img="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=400&auto=format&fit=crop"),
        SparePart(name="NGK Iridium Spark Plugs (x4)", brand="NGK",
                  category="Filters", price=4_800, stock=28,
                  img="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=400&auto=format&fit=crop"),
        SparePart(name="Castrol EDGE 5W-30 Engine Oil 5L", brand="Castrol",
                  category="Filters", price=3_600, stock=50,
                  img="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=400&auto=format&fit=crop"),
    ]
    db.add_all(parts)

    db.commit()
    print("✅  Database seeded — demo@masonautohub.com / demo1234")
