from database import Database


class Constants():
    DB_URL = "wss://test-med-069pe77i4lv4j3mhm6bc7t5u9g.aws-use1.surreal.cloud"
    DB_NAMESPACE = "embedding_example"
    DB_DATABASE = "embedding_example"
    DB_PARAMS = Database(DB_URL,DB_NAMESPACE,DB_DATABASE)


    THIS_FOLDER = "./"
    PREV_EXTRACTED_INGREDIENTS_FILE = THIS_FOLDER + "/extracted_ingredients_list.txt"
    MODEL_PATH = THIS_FOLDER + "/glove.6B.50d.txt"
    
    #https://www.kaggle.com/datasets/watts2/glove6b50dtxt
