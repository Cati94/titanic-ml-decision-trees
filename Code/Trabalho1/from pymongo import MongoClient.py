from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime, timedelta

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client["HS_db"]  # Replace with your database name
faker = Faker()

# Generate base data: Doentes
def generate_doentes(n=50):
    specialties = ["Pediatria", "Oncologia", "Ortopedia", "Queimados", "Cardiologia"]
    statuses = ["internado", "alta", "fila_espera"]
    doentes = []
    for _ in range(n):
        doente = {
            "nome": faker.name(),
            "data_nascimento": faker.date_of_birth(minimum_age=0, maximum_age=100),
            "especialidade": random.choice(specialties),
            "status": random.choice(statuses),
        }
        doentes.append(doente)
    return db.doentes.insert_many(doentes).inserted_ids

# Generate base data: Medicos
def generate_medicos(n=10):
    specialties = ["Pediatria", "Oncologia", "Ortopedia", "Queimados", "Cardiologia"]
    medicos = []
    for _ in range(n):
        medico = {
            "nome": faker.name(),
            "data_nascimento": faker.date_of_birth(minimum_age=30, maximum_age=60),
            "universidade": faker.company(),
            "numero_funcionario": faker.unique.random_number(digits=5),
            "data_admissao": faker.date_between(start_date='-10y', end_date='today'),
            "data_dispensado": None if random.random() > 0.3 else faker.date_between(start_date='-5y', end_date='today'),
            "especialidades": random.sample(specialties, random.randint(1, 2)),
        }
        medicos.append(medico)
    return db.medicos.insert_many(medicos).inserted_ids

# Generate base data: Quartos
def generate_quartos(n=20):
    alas = [{"_id": i, "nome": f"A{i}", "especialidade": random.choice(["Pediatria", "Oncologia"])} for i in range(1, 6)]
    db.alas.insert_many(alas)  # Insert alas first
    quartos = []
    for i in range(n):
        quarto = {
            "numero": i + 1,
            "ala_id": random.choice(alas)["_id"],
            "camas": random.randint(1, 6),
        }
        quartos.append(quarto)
    return db.quartos.insert_many(quartos).inserted_ids

# Generate related data: Internamentos
def generate_internamentos(n=30):
    doentes = list(db.doentes.find({"status": "internado"}))  # Only use "internado" patients
    quartos = list(db.quartos.find())
    medicos = list(db.medicos.find())
    internamentos = []
    for _ in range(n):
        doente = random.choice(doentes)
        quarto = random.choice(quartos)
        medico = random.choice(medicos)
        internamento = {
            "doente_id": doente["_id"],
            "quarto_id": quarto["_id"],
            "medico_id": medico["_id"],
            "causa_internamento": faker.sentence(),
            "data_entrada": faker.date_between(start_date='-1y', end_date='today'),
            "data_alta": None if random.random() > 0.7 else faker.date_between(start_date='-6m', end_date='today'),
        }
        internamentos.append(internamento)
    db.internamentos.insert_many(internamentos)
    print(f"Inserted {n} internamentos.")

# Generate related data: Intervencoes
def generate_intervencoes(n=50):
    internamentos = list(db.internamentos.find())
    medicos = list(db.medicos.find())
    intervencoes = []
    for _ in range(n):
        internamento = random.choice(internamentos)
        medico = random.choice(medicos)
        intervencao = {
            "internamento_id": internamento["_id"],
            "descricao": faker.sentence(),
            "data_hora_prevista": faker.date_time_between(start_date='now', end_date='+1y'),
            "medico_id": medico["_id"],
        }
        intervencoes.append(intervencao)
    db.intervencoes.insert_many(intervencoes)
    print(f"Inserted {n} intervencoes.")

# Run generators
if __name__ == "__main__":
    print("Generating base data...")
    generate_doentes(100)
    generate_medicos(20)
    generate_quartos(50)
    print("Generating related data...")
    generate_internamentos(50)
    generate_intervencoes(100)
    print("Data generation completed.")
