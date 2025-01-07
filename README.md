This repository provides a way to upload an embedding model to SurrealDB and use a SurQL SQL function to calculate embeddings within the database. The primary goal is to enable in-database vector calculations and searches without the need to pre-calculate vectors.

Here's a breakdown of the repository's key components:

*   **Embedding Model Upload:** The repository is designed to allow you to upload a pre-trained embedding model into SurrealDB. The example provided uses a GloVe embedding model. You can download the GloVe model from [https://nlp.stanford.edu/projects/glove/](https://nlp.stanford.edu/projects/glove/), and a specific version of this model is available at [https://www.kaggle.com/datasets/watts2/glove6b50dtxt](https://www.kaggle.com/datasets/watts2/glove6b50dtxt).
*   **SQL Function Creation:** A SurrealQL function is created to generate embeddings from text using the uploaded model. This function, named `fn::sentence_to_vector`, can be called within SurrealDB queries.
    *   **Example Function Call:** `return fn::sentence_to_vector("this is a test");` would return a vector of float values.
    *   **Auto Embedding Generation**: The `fn::sentence_to_vector` function can calculate embedding vectors on-the-fly when inserting data into the database. Specifically, you can define a table with a `description` field and a `description_embedding` field, and the `description_embedding` field can be automatically populated with the output of the `fn::sentence_to_vector` function when new records are inserted. This is done by setting a default value on the field definition.

        Here's the example code demonstrating how to do this:

        ```sql
        DEFINE TABLE some_table TYPE NORMAL SCHEMAFULL;
        DEFINE FIELD description ON some_table TYPE option<string>;
        DEFINE FIELD description_embedding ON TABLE some_table TYPE option<array<float>>
        DEFAULT fn::sentence_to_vector(description) ;
        ```

        * **Explanation of the code:**

            **`DEFINE TABLE some_table TYPE NORMAL SCHEMAFULL;`**: This line defines a table named `some_table` with a normal and schemaless type. This indicates that the table's structure is flexible and can accommodate various data types, and schemas can be enforced as needed.
            **`DEFINE FIELD description ON some_table TYPE option<string>;`**: This line defines a field named `description` within the `some_table`. It specifies that this field will store an optional string value.
            **`DEFINE FIELD description_embedding ON TABLE some_table TYPE option<array<float>>`**: This defines a field named `description_embedding` within the `some_table`. It specifies that this field will store an optional array of float values representing the embedding vector.
            **`DEFAULT fn::sentence_to_vector(description);`**: This crucial part sets the **default value** for the `description_embedding` field. Whenever a new record is inserted into `some_table` and the `description_embedding` field is not explicitly set, the database will automatically calculate the vector embedding of the `description` field using the `fn::sentence_to_vector` function, and store this result in the `description_embedding` field.

            * **Key takeaways:**
                * The `DEFAULT` keyword enables the automatic population of the `description_embedding` field with the output of the `fn::sentence_to_vector` function whenever a record is inserted without an explicit `description_embedding` value.
                * This approach allows for on-the-fly generation of vector embeddings during data insertion, making it easier to perform semantic searches.
                * By defining a default value, the database handles embedding calculations automatically without needing external processes or applications.



      *   **Vector Search Function:** Here is an example of a `fn::vector_search` function that performs a semantic search directly within the database. This function takes an input string, calculates its embedding vector using `fn::sentence_to_vector`, and then performs a k-nearest neighbors (KNN) search within the database based on pre-calculated embeddings.

      * ```sql
        DEFINE FUNCTION OVERWRITE fn::vector_search($input_string: string) {
            #returns 5 results based on brute force vector search
            LET $vector_embedding = fn::sentence_to_vector($input_string);
            LET $semantic_results = (
                SELECT *, vector::distance::knn() as distance
                FROM some_table
                WHERE description_embedding <|5|> $vector_embedding
                ORDER BY distance
            );
            RETURN $semantic_results;
        };
        ```
      
      **Key components of the function:**
      
      *   **`DEFINE FUNCTION OVERWRITE fn::vector_search($input_string: string)`**: This defines a function named `fn::vector_search` that accepts a string as input.
      *   **`LET $vector_embedding = fn::sentence_to_vector($input_string);`**: This line calculates the embedding vector of the input string using the `fn::sentence_to_vector` function, and stores it in the variable `$vector_embedding`.
      *   **`LET $semantic_results = (... );`**: This defines a variable `$semantic_results` that will store the results of the KNN search.
      *   **`SELECT *, vector::distance::knn() as distance FROM some_table`**: This selects all fields from the `some_table` along with the calculated distance using the `vector::distance::knn()` function, and aliases that column as `distance`.
      *   **`WHERE description_embedding <|5|> $vector_embedding`**: This filters the records in `some_table` to find the 5 nearest neighbors based on the calculated `$vector_embedding` using the `<|5|>` operator, that represents a k-nearest-neighbors search.
      *   **`ORDER BY distance`**: This orders the results by the calculated distance.
      *   **`RETURN $semantic_results;`**: This returns the results of the semantic search.
      
      This function enables you to perform semantic searches directly within the database, without needing to pre-calculate the vector embeddings. This means that when you have a new input string, you can find similar records based on the embeddings of their description fields directly using this function, making your search functionality more dynamic.




**Step-by-step instructions on how to run the code:**

1.  **Download an embedding model:** Download a pre-trained embedding model, such as the GloVe model, from [https://nlp.stanford.edu/projects/glove/](https://nlp.stanford.edu/projects/glove/) or the specific version from [https://www.kaggle.com/datasets/watts2/glove6b50dtxt](https://www.kaggle.com/datasets/watts2/glove6b50dtxt).
2.  **Set up your SurrealDB database:** Either install a version in your environment/laptop [https://surrealdb.com/docs/surrealdb/introduction/start](https://surrealdb.com/docs/surrealdb/introduction/start) or go the cloud route [https://surrealdb.com/cloud](https://surrealdb.com/cloud).
4.  **Environment Variables:** Ensure your SurrealDB credentials are set as environment variables.
3.  **Update `constants.py`:** Modify the `constants.py` file to include the path to your downloaded model and SurrealDB connection details.
5.  **Run the script:** Execute the `step_0_process_input_embedding_model.py` script. This script will upload the embedding model into SurrealDB. Please note that this step could take several hours depending on the size of the embedding model and the performance of your database.

The repository is designed to make it easier to perform complex database operations efficiently. The use of SurrealDB's features with the provided functions can enhance your ability to build and scale real-time applications. The use of SurrealML enables storage and execution of ML models, and allows for integration with external training frameworks.
