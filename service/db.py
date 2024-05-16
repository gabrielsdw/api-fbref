from pymongo.mongo_client import MongoClient

class MongoDbAtlasService:
    def __init__(self, user: str, password: str, name_db: str) -> None:
        self.user = user
        self.password = password
        
        self.url_connect = f"mongodb+srv://{user}:{password}@fbref.ykohrzq.mongodb.net/?retryWrites=true&w=majority&appName=fbref"
        
        self.client = MongoClient(self.url_connect, serverSelectionTimeoutMS=60000, connectTimeoutMS=60000, socketTimeoutMS=60000)
         
        self.db = self.client[name_db]
        
        self.collection = None

    
    def get_games_per_team(self, camp, team, number_games):
        self.collection = self.db[camp]
        
        condicoes = {"$or": [
        {"HomeTeam": team},
        {"AwayTeam": team}
        ]}
        
        dados = self.collection.find(condicoes)
         
        lista_dados = []
        for dado in dados:
            del dado['_id']
            lista_dados.append(dado)
        
        lista_dados = lista_dados[-number_games:]
        return lista_dados
    

    def get_disctinct_teams(self, camp):
        self.collection = self.db[camp]

        dados = self.collection.distinct('HomeTeam')
        dados = list(map(lambda x: x.lower(), dados))
        
        return dados
    

    def verify_connection(self):
        try:
            self.client.admin.command('ping')
        except Exception as e:
            print('Deu ruim')
            print(e)
        else:
            print('Deu bom')




if __name__ == '__main__':
    db = MongoDbAtlasService('gabrielsdw', '54321', 'fbref')
    
    #db.verify_connection()
    print(db.get_disctinct_teams('PremierLeague'))
    print(db.get_disctinct_teams('LaLiga'))
    print(db.get_disctinct_teams('BundesLiga'))