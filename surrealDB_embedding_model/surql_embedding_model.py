from surrealdb import AsyncSurreal

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
      outcome = await self.db.query(SurqlEmbeddingModel.INSERT_EMBEDDING, params)
      for item in outcome:
          if item["status"]=="ERR":
              raise SystemError("Step action error: {0}".format(item["result"])) 
      return outcome
  
  async def get_model_dimensions(self):
      outcome = await self.db.query("SELECT VALUE array::len(embedding) FROM embedding_model LIMIT 1")
      return int(outcome[0]["result"][0])


