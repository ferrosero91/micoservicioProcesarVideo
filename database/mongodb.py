from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import Config


class MongoDBClient:
    """MongoDB client singleton"""
    
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._connect()
    
    def _build_connection_uri(self):
        """Build MongoDB connection URI from config"""
        if Config.MONGODB_USERNAME and Config.MONGODB_PASSWORD:
            # With authentication
            uri = (
                f"mongodb://{Config.MONGODB_USERNAME}:{Config.MONGODB_PASSWORD}"
                f"@{Config.MONGODB_HOST}:{Config.MONGODB_PORT}/"
                f"{Config.MONGODB_DATABASE}?authSource={Config.MONGODB_AUTH_DATABASE}"
            )
        else:
            # Without authentication (local development)
            uri = f"mongodb://{Config.MONGODB_HOST}:{Config.MONGODB_PORT}/"
        
        return uri
    
    def _connect(self):
        """Connect to MongoDB"""
        try:
            connection_uri = self._build_connection_uri()
            
            # Hide password in logs
            safe_uri = connection_uri.replace(
                f":{Config.MONGODB_PASSWORD}@" if Config.MONGODB_PASSWORD else "",
                ":****@" if Config.MONGODB_PASSWORD else ""
            )
            
            self._client = MongoClient(
                connection_uri,
                serverSelectionTimeoutMS=5000
            )
            
            # Test connection
            self._client.admin.command('ping')
            print(f"Connected to MongoDB: {safe_uri}")
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            print("Using default prompts from code")
            self._client = None
        except Exception as e:
            print(f"Unexpected error connecting to MongoDB: {e}")
            print("Using default prompts from code")
            self._client = None
    
    @property
    def client(self):
        return self._client
    
    @property
    def database(self):
        if self._client:
            return self._client[Config.MONGODB_DATABASE]
        return None
    
    def is_connected(self):
        return self._client is not None
