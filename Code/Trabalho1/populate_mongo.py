from pymongo import MongoClient
from faker import Faker
from bson import ObjectId
import random

# Initialize Faker and MongoDB client
faker = Faker()
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client["hospital_db"]  # Replace with your database name

# Function to generate and insert data into the 'alas' collection
def generate_alas(n=5):
    specialties = ["Pediatria", "Oncologia", "Ortopedia", "Queimados", "Cardiologia"]
    alas = []
    for _ in range(n):
        ala = {
            "nome": f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(1, 9)}",
            "especialidade": random.choice(specialties),
        }
        alas.append(ala)
    result = db.alas.insert_many(alas)
    print(f"Inserted {n} alas. IDs: {result.inserted_ids}")

# Function to generate and insert data into the 'quartos' collection
def generate_quartos(n=20):
    alas = list(db.alas.find())  # Fetch all 'alas' documents
    quartos = []
    for _ in range(n):
        ala = random.choice(alas)
        quarto = {
            "numero": random.randint(1, 100),
            "ala_id": ala["_id"],  # Reference to an 'ala'
            "camas": random.randint(1, 6),
        }
        quartos.append(quarto)
    result = db.quartos.insert_many(quartos)
    print(f"Inserted {n} quartos. IDs: {result.inserted_ids}")

# Main function
if __name__ == "__main__":
    print("Generating data...")
    generate_alas(10)
    generate_quartos(50)
    print("Data generation complete.")
