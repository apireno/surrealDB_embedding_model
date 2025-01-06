from embeddings import EmbeddingModel
from surrealdb import AsyncSurrealDB

class SurqlEmbeddingModel:
  


  INSERT_EMBEDDING = """
  LET $this_object = type::thing("embedding_model",$word);
  CREATE $this_object  CONTENT {
      word : $word,
      embedding:  $embedding
      } RETURN NONE;
  """

  def __init__(self,db: AsyncSurrealDB):
      self.db = db

  async def insert_embedding(self,word,embedding):
      params = {"word": word,"embedding": embedding}
      outcome = await self.db.query(SurqlEmbeddingModel.INSERT_EMBEDDING, params)
      for item in outcome:
          if item["status"]=="ERR":
              raise SystemError("Step action error: {0}".format(item["result"])) 
      return outcome


