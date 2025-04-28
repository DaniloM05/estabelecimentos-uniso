import os
from dotenv import load_dotenv 
from pymongo import MongoClient 

# Carregar variáveis do .env
load_dotenv()

# Obter a URI do MongoDB do .env
MONGO_URI = os.getenv("MONGO_URI")

# Conectar ao MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["estabelecimentosDB"]  # Nome do banco de dados

# Criar índice geoespacial na coleção de estabelecimentos
collection = db["estabelecimentos"]
collection.create_index([("location", "2dsphere")])  # Índice geoespacial

print("Conexão com MongoDB estabelecida!")
