from database import Database


class Constants():
    #The path to your SurrealDB instance
    DB_URL = "wss://xxxx"
    #The the SurrealDB namespace and database to upload the model to
    DB_NAMESPACE = "embedding_example"
    DB_DATABASE = "embedding_example"
    #Wrap the parameters in a class
    DB_PARAMS = Database(DB_URL,DB_NAMESPACE,DB_DATABASE)
    #For use in authenticating your database in database.py
    #These are just the pointers to the environment variables
    #Don't put the actual passwords here
    DB_USER_ENV_VAR = "SURREAL_CLOUD_TEST_USER"
    DB_PASS_ENV_VAR = "SURREAL_CLOUD_TEST_PASS"


    THIS_FOLDER = "./"
    
    #You must download a model in the format of:
    # word v1 v2 v3 ... vN
    #here is an example
    #https://www.kaggle.com/datasets/watts2/glove6b50dtxt
    MODEL_PATH = THIS_FOLDER + "/glove.6B.50d.txt"
