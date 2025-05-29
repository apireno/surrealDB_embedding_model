import time
import asyncio
import pandas as pd
from surrealdb import Surreal
from surrealDB_embedding_model.embedding_model_ddl import EmbeddingModelDDL
from surrealDB_embedding_model.surql_embedding_model import SurqlEmbeddingModel
from surrealDB_embedding_model.embedding_model_constants import EmbeddingModelConstants,DatabaseConstants,THIS_FOLDER,ArgsLoader
import numpy as np
from surrealDB_embedding_model.embeddings import EmbeddingModel
from surrealDB_embedding_model.database import Database
import tqdm


out_folder = THIS_FOLDER + "/embeddings_{0}".format(time.strftime("%Y%m%d-%H%M%S"))
db_constants = DatabaseConstants()
embed_constants = EmbeddingModelConstants()
args_loader = ArgsLoader("Input Embeddings Model",db_constants,embed_constants)
args_loader.LoadArgs()

CHUNK_SIZE = 1000 # Size of chunks for batch insertion


INSERT_EMBEDDINGS = """
    FOR $row IN $embeddings {
        CREATE type::thing("embedding_model",$row.word)  CONTENT {
        word : $row.word,
        embedding: $row.embedding
        } RETURN NONE;
    };
"""



def surreal_model_insert(embeddingModel):
   

    with Surreal(db_constants.DB_PARAMS.url) as db:


        db.signin({"username": db_constants.DB_PARAMS.username, "password": db_constants.DB_PARAMS.password})


        print("Connected to SurrealDB")
        print("Creating namespace and database if not exists")
        outcome = Database.ParseResponseForErrors(db.query_raw(EmbeddingModelDDL.DDL_CREATE_NS.format(ns=db_constants.DB_PARAMS.namespace,db=db_constants.DB_PARAMS.database)))
       
        db.use(db_constants.DB_PARAMS.namespace, db_constants.DB_PARAMS.database)
        print("Creating tables and functions")
        Database.ParseResponseForErrors(
            outcome = Database.ParseResponseForErrors(db.query_raw(EmbeddingModelDDL.DDL_EMBEDDING_MODEL))
        )
        embeddings_df = pd.DataFrame({'word': embeddingModel.dictionary.keys(), 'embedding': embeddingModel.dictionary.values()})


        print("Embeddings Model Description Len")
        print(len(embeddings_df))
        print("Embeddings Model Description Head")
        embeddings_df["len"] = embeddings_df["embedding"].apply(len)  
        print(embeddings_df.sort_values(by=['len']).head()) 

        # Calculate number of chunks for batch processing.
        total_rows = len(embeddings_df)
        total_chunks = (total_rows + CHUNK_SIZE - 1) // CHUNK_SIZE  # Calculate number of chunks for batch processing


        print("Inserting rows into SurrealDB")

        with tqdm.tqdm(total=total_chunks, desc="Inserting") as pbar:
            # Iterate through chunks of data.
            for i in range(0, total_rows, CHUNK_SIZE):
                # Get a chunk of data.
                chunk = embeddings_df.iloc[i:i + CHUNK_SIZE]
                # create an array of dicts to bulk load into surreal
                formatted_rows = [
                    {
                        "word": EmbeddingModel.unescape_token_text_for_txt_file(str(row["word"])),
                        "embedding":row["embedding"].tolist()
                    }
                    for _, row in chunk.iterrows()
                ]

                # Insert the chunk.
                Database.ParseResponseForErrors(db.query_raw(
                    INSERT_EMBEDDINGS, params={"embeddings": formatted_rows}
                ))
                # Update progress bar.
                pbar.update(1)




async def main():

    print("""
          STEP 0
          DB_PARAMS {URL} N: {NS} DB: {DB} USER: {DB_USER}

          DB_USER_ENV_VAR {DB_USER_ENV_VAR}
          DB_PASS_ENV_VAR {DB_PASS_ENV_VAR}

          MODEL_PATH {MODEL_PATH}
          """.format(
              URL = db_constants.DB_PARAMS.url,
              DB_USER = db_constants.DB_PARAMS.username,
              NS = db_constants.DB_PARAMS.namespace,
              DB = db_constants.DB_PARAMS.database,
              DB_USER_ENV_VAR = db_constants.DB_USER_ENV_VAR,
              DB_PASS_ENV_VAR = db_constants.DB_PASS_ENV_VAR,
              MODEL_PATH = embed_constants.MODEL_PATH
          )
          )
    
    


    surreal_model_insert(EmbeddingModel(embed_constants.MODEL_PATH))
    



if __name__ == "__main__":
    asyncio.run(main())


    
