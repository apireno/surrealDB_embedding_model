from surrealdb import AsyncSurreal
from surrealDB_embedding_model.database import Database

class SurqlEmbeddingModel:
  
  INSERT_EMBEDDING = """
  LET $this_object = type::thing("embedding_model",$word);
  CREATE $this_object  CONTENT {
      word : $word,
      embedding:  $embedding
      } RETURN NONE;
  """

  def __init__(self,db: AsyncSurreal):
      self.db = db

  async def insert_embedding(self,word,embedding):
      params = {"word": word,"embedding": embedding}
      outcome = Database.ParseResponseForErrors(await self.db.query_raw(SurqlEmbeddingModel.INSERT_EMBEDDING, params))
      return outcome
  
  async def get_model_dimensions(self):
      outcome = Database.ParseResponseForErrors(await self.db.query_raw("SELECT VALUE array::len(embedding) FROM embedding_model LIMIT 1"))
      return int(outcome[0]["result"][0])


