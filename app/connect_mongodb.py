
from pymongo import MongoClient
from jproperties import Properties



class Connect_MongoDB:


    def __init__(self):
        
        p = Properties()
        with open("app/app.properties", 'r+b') as f:
            p.load(f)

        self.user = p.get('mongodb_user').data
        self.password = p.get('mongodb_password').data
        self.host = p.get('mongodb_host').data
        self.port = p.get('mongodb_port').data


    def _connect_(self):
        
        self.client = MongoClient(username = self.user, 
                             password = self.password, 
                             host = self.host, 
                             port = int(self.port))    
        self.db = self.client.get_database('zap_imoveis')

        return self.db


    def connect(self):

        return self._connect_()

