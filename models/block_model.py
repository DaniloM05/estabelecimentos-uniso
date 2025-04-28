import hashlib
import json

class Block:
    def __init__(self, id_bloco, dados, hash_anterior='0'):
        self.id_bloco = id_bloco
        self.dados = dados
        self.hash_anterior = hash_anterior
        self.hash_atual = self.gerar_hash()

    def gerar_hash(self):
        bloco_string = json.dumps({
            'id_bloco': self.id_bloco,
            'dados': self.dados,
            'hash_anterior': self.hash_anterior
        }, sort_keys=True).encode()
        return hashlib.sha256(bloco_string).hexdigest()

    def to_dict(self):
        return {
            'id_bloco': self.id_bloco,
            'dados': self.dados,
            'hash_anterior': self.hash_anterior,
            'hash_atual': self.hash_atual
        }
