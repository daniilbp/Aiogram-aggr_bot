from pymongo import MongoClient
from pymongo.server_api import ServerApi

from additions.p_conf import MONGO_USER, MONGO_PASSWORD, MONGO_CLUSTER


def connect_local():
    """Функция для локального подключения к MongoDB"""
    # client = MongoClient() #Подключение по умолчанию
    # client = MongoClient("localhost", 27017) #Подключение по умолчанию явно
    client = MongoClient("mongodb://localhost:27017/") #используя формат URI MongoDB

    return client


def connect_atlas(user: str = MONGO_USER, password: str = MONGO_PASSWORD, cluster: str = MONGO_CLUSTER):
    """Функция для подключения к MongoDB ч/з кластер в Атласе"""
    uri = f"mongodb+srv://{user}:{password}@{cluster}.mongodb.net"
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!\n")
    except Exception as e:
        print(e)
    
    return client
