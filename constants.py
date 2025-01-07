
import argparse
import os
from database import Database

class Constants():
    THIS_FOLDER = "./"

    def __init__(self):
       

        #export SURREAL_CLOUD_TEST_USER=xxx
        #export SURREAL_CLOUD_TEST_PASS=xxx

        self.DB_USER_ENV_VAR = "SURREAL_CLOUD_TEST_USER"
        self.DB_PASS_ENV_VAR = "SURREAL_CLOUD_TEST_PASS"
        
        
        #The path to your SurrealDB instance
        #The the SurrealDB namespace and database to upload the model to
        self.DB_PARAMS = Database(
            "ws://0.0.0.0:8000",
            os.getenv(self.DB_USER_ENV_VAR),
            os.getenv(self.DB_PASS_ENV_VAR),
            "embedding_example",
            "embedding_example")
                    
        


        #For use in authenticating your database in database.py
        #These are just the pointers to the environment variables
        #Don't put the actual passwords here




        
        #You must download a model in the format of:
        # word v1 v2 v3 ... vN
        #here is an example
        #https://www.kaggle.com/datasets/watts2/glove6b50dtxt
        self.MODEL_PATH = Constants.THIS_FOLDER + "/glove.6B.50d.txt"

    def LoadArgs(self,description):

        parser = argparse.ArgumentParser(description=description)
        parser.add_argument("-url","--url", help="Path to your SurrealDB instance (Default: {0})".format(self.DB_PARAMS.url))
        parser.add_argument("-ns","--namespace", help="SurrealDB namespace to create and install the model (Default: {0})".format(self.DB_PARAMS.namespace))
        parser.add_argument("-db","--database", help="SurrealDB database to create and install the model (Default: {0})".format(self.DB_PARAMS.database))
        parser.add_argument("-mp","--model_path", help="Your model file (Default: {0})".format(self.MODEL_PATH))
        parser.add_argument("-uenv","--user_env", help="Your environment variable for db username (Default: {0})".format(self.DB_USER_ENV_VAR))
        parser.add_argument("-penv","--pass_env", help="Your environment variable for db password (Default: {0})".format(self.DB_PASS_ENV_VAR))
        
        args = parser.parse_args()

        if args.url:
            self.DB_PARAMS.url = args.url
        if args.namespace:
            self.DB_PARAMS.namespace = args.namespace
        if args.database:
            self.DB_PARAMS.database = args.database
        if args.model_path:
            self.MODEL_PATH = args.model_path
        if args.user_env:
            self.DB_USER_ENV_VAR = args.user_env
            self.DB_PARAMS.username = os.getenv(self.DB_USER_ENV_VAR)
        if args.pass_env:
            self.DB_PASS_ENV_VAR = args.pass_env
            self.DB_PARAMS.password = os.getenv(self.DB_PASS_ENV_VAR)

        

    
