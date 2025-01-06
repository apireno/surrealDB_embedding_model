from database import Database


class Constants():
    DB_URL = "wss://xxxx"
    DB_NAMESPACE = "embedding_example"
    DB_DATABASE = "embedding_example"
    DB_PARAMS = Database(DB_URL,DB_NAMESPACE,DB_DATABASE)


    THIS_FOLDER = "./"
    PREV_EXTRACTED_INGREDIENTS_FILE = THIS_FOLDER + "/extracted_ingredients_list.txt"
    #You must download a model in the format of:
    # word v1 v2 v3 ... vN
    #here is an example
    #https://www.kaggle.com/datasets/watts2/glove6b50dtxt
    MODEL_PATH = THIS_FOLDER + "/glove.6B.50d.txt"
