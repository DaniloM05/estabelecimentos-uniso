from models.estabelecimento_model import Estabelecimento
from services import blockchain_service
from pymongo import MongoClient
from geopy.distance import geodesic
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)

try:
    client.admin.command('ping')
    print("✅ Conexão com o MongoDB estabelecida com sucesso!")
except Exception as e:
    print(f"❌ Erro ao conectar ao MongoDB: {e}")

db = client["estabelecimentosDB"]
collection = db["estabelecimentos"]


def cadastrar_estabelecimento(estabelecimento):
    if not validar_distancia(estabelecimento.latitude, estabelecimento.longitude):
        return False, f"Estabelecimento muito próximo de outro. Distância mínima de 2km é necessária."

    if buscar_por_nome(estabelecimento.nome):
        return False, "Já existe um estabelecimento com esse nome."

    # Insere no MongoDB
    collection.insert_one({
        "nome": estabelecimento.nome,
        "location": {
            "type": "Point",
            "coordinates": [estabelecimento.longitude, estabelecimento.latitude]
        }
    })

    # Agora adiciona no blockchain também
    blockchain_service.adicionar_bloco({
        "nome": estabelecimento.nome,
        "latitude": estabelecimento.latitude,
        "longitude": estabelecimento.longitude
    })

    return True, "Estabelecimento cadastrado com sucesso!"

def listar_estabelecimentos():
    return list(collection.find({}, {"_id": 0}))


def validar_distancia(lat, lon):
    estabelecimentos = collection.find({})
    for est in estabelecimentos:
        coords = est["location"]["coordinates"]
        dist = geodesic((lat, lon), (coords[1], coords[0])).km
        if dist < 2:
            return False
    return True


def relatorio_10km():
    resultado = []
    estabelecimentos = list(collection.find({}))
    for est in estabelecimentos:
        nome = est["nome"]
        coords = est["location"]["coordinates"]
        raio_km = 10
        raio_em_radianos = raio_km / 6378.1

        proximos = collection.count_documents({
            "location": {
                "$geoWithin": {
                    "$centerSphere": [coords, raio_em_radianos]
                }
            },
            "nome": {"$ne": nome}
        })

        resultado.append({
            "estabelecimento": nome,
            "quantidade_proximos_10km": proximos
        })
    return resultado


def relatorio_5km_por_nome(nome):
    est = collection.find_one({"nome": nome})
    if not est:
        return [], f"Estabelecimento '{nome}' não encontrado."

    coords = est["location"]["coordinates"]
    raio_km = 5
    raio_em_radianos = raio_km / 6378.1

    proximos = collection.find({
        "location": {
            "$geoWithin": {
                "$centerSphere": [coords, raio_em_radianos]
            }
        },
        "nome": {"$ne": nome}
    })

    return [p["nome"] for p in proximos], None


def mais_proximo_de_ponto(lat, lon):
    estabelecimentos = list(collection.find({}))
    if not estabelecimentos:
        return None, "Nenhum estabelecimento cadastrado."

    menor = float("inf")
    mais_proximo = None

    for est in estabelecimentos:
        coords = est["location"]["coordinates"]
        dist = geodesic((lat, lon), (coords[1], coords[0])).km
        if dist < menor:
            menor = dist
            mais_proximo = est

    return {
        "mais_proximo": mais_proximo["nome"],
        "distancia_km": round(menor, 2)
    }, None


def buscar_por_nome(nome):
    return collection.find_one({"nome": nome})


def editar_estabelecimento(nome_antigo, novo_estabelecimento):
    existente = buscar_por_nome(nome_antigo)
    if not existente:
        return False, f"Estabelecimento '{nome_antigo}' não encontrado."

    if nome_antigo != novo_estabelecimento.nome and buscar_por_nome(novo_estabelecimento.nome):
        return False, f"Já existe um estabelecimento com o nome '{novo_estabelecimento.nome}'."

    estabelecimentos = collection.find({"nome": {"$ne": nome_antigo}})
    for est in estabelecimentos:
        coords = est["location"]["coordinates"]
        dist = geodesic((novo_estabelecimento.latitude, novo_estabelecimento.longitude), (coords[1], coords[0])).km
        if dist < 2:
            return False, f"Estabelecimento muito próximo de '{est['nome']}'. Distância mínima de 2km é necessária."

    collection.update_one(
        {"nome": nome_antigo},
        {"$set": {
            "nome": novo_estabelecimento.nome,
            "location": {
                "type": "Point",
                "coordinates": [novo_estabelecimento.longitude, novo_estabelecimento.latitude]
            }
        }}
    )
    return True, "Estabelecimento atualizado com sucesso!"


def excluir_estabelecimento(nome):
    resultado = collection.delete_one({"nome": nome})
    if resultado.deleted_count == 0:
        return False, f"Estabelecimento '{nome}' não encontrado."
    return True, "Estabelecimento excluído com sucesso!"
