import time
import asyncio
from surrealdb import AsyncSurrealDB
import pandas as pd
from surql_ddl import SurqlDDL
from surql_embedding_model import SurqlEmbeddingModel
from constants import Constants
import numpy as np
from embeddings import EmbeddingModel

out_folder = Constants.THIS_FOLDER + "/embeddings_{0}".format(time.strftime("%Y%m%d-%H%M%S"))
constants = Constants()
constants.LoadArgs("Input Embeddings Model")

embeddding_insert_durations = []

async def process_embedding(dataProcessor:SurqlEmbeddingModel,row,counter,total_count,start_time):
    percentage = counter/total_count
    method_start_time = time.time() 

    out = await dataProcessor.insert_embedding(row.word,row.embedding.tolist())
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
    async with AsyncSurrealDB(constants.DB_PARAMS.url) as db:

        auth_token = await db.sign_in(constants.DB_PARAMS.username,constants.DB_PARAMS.password)
        outcome = await db.query(SurqlDDL.DDL_OVERWRITE_NS.format(ns=constants.DB_PARAMS.namespace,db=constants.DB_PARAMS.database))
        await db.use(constants.DB_PARAMS.namespace, constants.DB_PARAMS.database)
        out = await db.query(SurqlDDL.DDL_EMBEDDING_MODEL)

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
              URL = constants.DB_PARAMS.url,
              DB_USER = constants.DB_PARAMS.username,
              NS = constants.DB_PARAMS.namespace,
              DB = constants.DB_PARAMS.database,
              DB_USER_ENV_VAR = constants.DB_USER_ENV_VAR,
              DB_PASS_ENV_VAR = constants.DB_PASS_ENV_VAR,
              MODEL_PATH = constants.MODEL_PATH
          )
          )
    
    embeddingModel = EmbeddingModel(constants.MODEL_PATH)
    embeddings_df = pd.DataFrame({'word': embeddingModel.dictionary.keys(), 'embedding': embeddingModel.dictionary.values()})

    print(embeddings_df.head())

    await process_embeddings(embeddings_df)



if __name__ == "__main__":
    asyncio.run(main())


    