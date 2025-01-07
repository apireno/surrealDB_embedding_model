
import os
from constants import Constants



#export SURREAL_CLOUD_TEST_USER=xxx
#export SURREAL_CLOUD_TEST_PASS=xxx

class Database():
    def __init__(self,url,namespace = None,database = None):
        self.username = os.getenv(Constants.DB_USER_ENV_VAR)
        self.password = os.getenv(Constants.DB_PASS_ENV_VAR)
        self.url = url
        self.namespace = namespace
        self.database = database
   

