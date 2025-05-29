
class EmbeddingModelDDL:

    DDL_CREATE_NS = """
        DEFINE NAMESPACE IF NOT EXISTS {ns};
        USE NAMESPACE {ns};
        DEFINE DATABASE IF NOT EXISTS {db};
        USE DATABASE {db};
    """
    DDL_OVERWRITE_NS = """
        DEFINE NAMESPACE OVERWRITE {ns};
        USE NAMESPACE {ns};
        DEFINE DATABASE OVERWRITE {db};
        USE DATABASE {db};
    """

    DDL_EMBEDDING_MODEL = """


        REMOVE TABLE IF EXISTS embedding_model;
        DEFINE TABLE embedding_model TYPE NORMAL SCHEMAFULL;
        DEFINE FIELD word ON embedding_model TYPE string;
        DEFINE FIELD embedding ON embedding_model TYPE array<float>;

       
        DEFINE FUNCTION OVERWRITE fn::retrieve_vectors_for_sentence($sentence:string) 
        {
            LET $sentence = $sentence.lowercase().
                replace('.',' .').
                replace(',',' ,').
                replace('?',' ?').
                replace('!',' !').
                replace(';',' ;').
                replace(':',' :').
                replace('(',' (').
                replace(')',' )').
                replace('[',' [').
                replace(']',' ]').
                replace('{',' {').
                replace('}',' }').
                replace('"',' "').
                replace("'"," '").
                replace('`',' `').
                replace('/',' /').
                replace('\\\\',' \\\\').
                replace('<',' <').
                replace('>',' >').
                replace('—',' —').
                replace('–',' –');
            LET $words = $sentence.words();
            LET $words = array::filter($words, |$word: any| $word != '');   

            #select the vectors from the embedding table that match the words
            
            RETURN (SELECT VALUE type::thing("embedding_model",$this).embedding FROM $words);
        };

        
        DEFINE FUNCTION OVERWRITE fn::sentence_to_vector($sentence: string) {
            
            #Pull the first row to determine the size of the vector (they should all be the same)
            LET $vector_size = (SELECT VALUE array::len(embedding) FROM embedding_model LIMIT 1)[0];
            
            #select the vectors from the embedding table that match the words
            LET $vectors = fn::retrieve_vectors_for_sentence($sentence);

            #remove any non-matches
            LET $vectors = array::filter($vectors, |$v| { RETURN $v != NONE; });
            
            #transpose the vectors to be able to average them
            LET $transposed = array::transpose($vectors);

            #sum up the individual floats in the arrays
            LET $sum_vector = $transposed.map(|$sub_array| math::sum($sub_array));

            # calculate the mean of each vector by dividing by the total number of 
            # vectors in each of the floats
            LET $mean_vector = vector::scale($sum_vector, 1.0 / array::len($vectors));

            #if the array size is correct return it, otherwise return array of zeros
            RETURN 
                IF array::len($mean_vector) == $vector_size THEN 
                    $mean_vector
                ELSE 
                    None
                END;
        };

    """


