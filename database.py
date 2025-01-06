
import os



#export SURREAL_CLOUD_TEST_USER=xxx
#export SURREAL_CLOUD_TEST_PASS=xxx

class Database():
    def __init__(self,url,namespace = None,database = None):
        self.username = os.getenv('SURREAL_CLOUD_TEST_USER')
        self.password = os.getenv('SURREAL_CLOUD_TEST_PASS')
        self.url = url
        self.namespace = namespace
        self.database = database
   

