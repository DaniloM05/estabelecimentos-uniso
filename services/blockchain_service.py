import hashlib
import json
from datetime import datetime

# Iniciamos a blockchain como uma lista vazia
blockchain = []

def criar_bloco(dados, anterior_hash=""):
    bloco = {
        'index': len(blockchain) + 1,
        'timestamp': str(datetime.utcnow()),
        'dados': dados,
        'anterior_hash': anterior_hash,
        'hash': ''
    }
    # Gera o hash do bloco depois de montar
    bloco['hash'] = gerar_hash(bloco)
    return bloco

def gerar_hash(bloco):
    bloco_str = json.dumps({
        'index': bloco['index'],
        'timestamp': bloco['timestamp'],
        'dados': bloco['dados'],
        'anterior_hash': bloco['anterior_hash']
    }, sort_keys=True).encode()

    return hashlib.sha256(bloco_str).hexdigest()

def adicionar_bloco(dados):
    anterior_hash = blockchain[-1]['hash'] if blockchain else '0'
    bloco = criar_bloco(dados, anterior_hash)
    blockchain.append(bloco)

def validar_blockchain():
    for i in range(1, len(blockchain)):
        bloco_atual = blockchain[i]
        bloco_anterior = blockchain[i-1]

        if bloco_atual['anterior_hash'] != bloco_anterior['hash']:
            return False

        if bloco_atual['hash'] != gerar_hash(bloco_atual):
            return False
    return True

def obter_blockchain():
    return blockchain
