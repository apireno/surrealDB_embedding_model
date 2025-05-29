import time
import asyncio
import pandas as pd
from surrealdb import AsyncSurreal
from surrealDB_embedding_model.embedding_model_ddl import EmbeddingModelDDL
from surrealDB_embedding_model.surql_embedding_model import SurqlEmbeddingModel
from surrealDB_embedding_model.embedding_model_constants import EmbeddingModelConstants,DatabaseConstants,THIS_FOLDER,ArgsLoader
import numpy as np
from surrealDB_embedding_model.embeddings import EmbeddingModel
from surrealDB_embedding_model.database import Database


out_folder = THIS_FOLDER + "/embeddings_{0}".format(time.strftime("%Y%m%d-%H%M%S"))
db_constants = DatabaseConstants()
embed_constants = EmbeddingModelConstants()
args_loader = ArgsLoader("Input Embeddings Model",db_constants,embed_constants)
args_loader.LoadArgs()

embeddding_insert_durations = []

async def process_embedding(dataProcessor:SurqlEmbeddingModel,row,counter,total_count,start_time):
    percentage = counter/total_count
    method_start_time = time.time() 

    outcome = Database.ParseResponseForErrors(await dataProcessor.insert_embedding(row.word,row.embedding.tolist()))
    current_time = time.time()
    
    elapsed_duration = current_time - start_time
    elapsed_duration_minutes = elapsed_duration/60
    average_duration = elapsed_duration / counter if counter else 0
    average_duration_ms = average_duration * 1000


    this_method_duration = current_time - method_start_time
    this_method_duration_ms = this_method_duration * 1000

    embeddding_insert_durations.append(this_method_duration)


    est_time_remaining = average_duration * (total_count - counter)
    est_time_remaining_minutes = est_time_remaining / 60
    

    print("inserting... {counter}/{total_count}\t{percent}\test\t{est_time_remaining}\telap\t{elapsed_duration}\tlast\t{this_method_duration}\tavg\t{average_duration}\t-{row}                                           ".format(
                counter = counter,
                total_count = total_count,
                percent = f"{percentage:.2%}",
                elapsed_duration = f"{elapsed_duration_minutes:.1f} min",
                average_duration = f"{average_duration_ms:.3f} ms",
                this_method_duration = f"{this_method_duration_ms:.3f} ms",
                est_time_remaining = f"{est_time_remaining_minutes:.1f} min",
                row = row.word
                ), end="\r", flush=True) 
    

async def process_embeddings(embeddings_df,batch_size=1,total_records=0,offset=0):

    if total_records==0 :
        total_records = len(embeddings_df)
    start_time = time.time()
    async with AsyncSurreal(db_constants.DB_PARAMS.url) as db:

        auth_token = await db.signin({"username":db_constants.DB_PARAMS.username,"password":db_constants.DB_PARAMS.password})

        
        outcome = Database.ParseResponseForErrors(await db.query_raw(EmbeddingModelDDL.DDL_OVERWRITE_NS.format(ns=db_constants.DB_PARAMS.namespace,db=db_constants.DB_PARAMS.database)))
        await db.use(db_constants.DB_PARAMS.namespace, db_constants.DB_PARAMS.database)
        outcome = Database.ParseResponseForErrors(await db.query_raw(EmbeddingModelDDL.DDL_EMBEDDING_MODEL))

        dataProcessor = SurqlEmbeddingModel(db)


        for i in range(offset, total_records, batch_size):
            batch = embeddings_df[i : i + batch_size].itertuples()
            tasks = [process_embedding(dataProcessor,row,i,total_records,start_time) for row in batch]
            await asyncio.gather(*tasks)



    
    current_time = time.time() 
    elapsed_duration = current_time - start_time
    elapsed_duration_minutes = elapsed_duration/60
    average_duration = elapsed_duration / total_records if total_records else 0
    average_duration_ms = average_duration * 1000
    
    min_embeddding_insert_duration = np.min(embeddding_insert_durations)
    min_embeddding_insert_duration_ms = min_embeddding_insert_duration * 1000

    max_embeddding_insert_duration = np.max(embeddding_insert_durations)
    max_embeddding_insert_duration_ms = max_embeddding_insert_duration * 1000



    print(
        """ 
        Step 0 -- Embedding Model Insertion                                                                                                        
        total elapsed {elapsed_duration}                                                                                                         
        {total_records} insert embbeding transaction (avg,min,max) ({average_duration},{min_embeddding_insert_duration},{max_embeddding_insert_duration})                                                     
        """.format(
        elapsed_duration = f"{elapsed_duration_minutes:.1f} min",
        average_duration = f"{average_duration_ms:.3f} ms",
        min_embeddding_insert_duration = f"{min_embeddding_insert_duration_ms:.3f} ms",
        max_embeddding_insert_duration = f"{max_embeddding_insert_duration_ms:.3f} ms",
        total_records = total_records 
        )) 


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
    
    embeddingModel = EmbeddingModel(embed_constants.MODEL_PATH)
    embeddings_df = pd.DataFrame({'word': embeddingModel.dictionary.keys(), 'embedding': embeddingModel.dictionary.values()})

    
    print("Embeddings Model Description Len")
    print(len(embeddings_df))
    print("Embeddings Model Description Head")
    embeddings_df["len"] = embeddings_df["embedding"].apply(len)  
    print(embeddings_df.sort_values(by=['len']).head()) 

    

    await process_embeddings(embeddings_df)



if __name__ == "__main__":
    asyncio.run(main())


    
