class Estabelecimento:
    def __init__(self, nome, latitude, longitude):
        self.nome = nome
        self.latitude = latitude
        self.longitude = longitude

    def to_document(self):
        return {
            "nome": self.nome,
            "location": {
                "type": "Point",
                "coordinates": [self.longitude, self.latitude]
            }
        }