import numpy as np
import gzip
import re

PUNCTUATION_TO_SEPARATE = [
                ".", ",", "?", "!", ";", ":", "(", ")", "[", "]", "{", "}", "\"", "'", "`", "/", "\\", "<", ">", "—", "–"
            ]


class EmbeddingModel:

    # Preprocess token text
    staticmethod
    def process_token_text_for_txt_file(text:str) ->str:
        """
        Preprocesses text for storage in a text-based embedding file.

        This method converts text to lowercase, removes punctuation, normalizes whitespace,
        and escapes spaces with a special character (!).

        Args:
            text (str): The text to preprocess.

        Returns:
            str: The preprocessed text.
        """

        token = str(text).lower()
        token = re.sub(r'[^\w\s]', '', token)  # Remove punctuation
        token = re.sub(r'\s+', ' ', token)  # Normalize whitespace (replace multiple spaces, tabs, newlines with a single ' ')
        token = token.strip()
        token = token.replace(" ","!") # escape character should be no punctuation
        return token
    
    
    # Preprocess token text (example - adjust as needed)
    staticmethod
    def unescape_token_text_for_txt_file(text:str) ->str:

        """
        Unescapes text read from a text-based embedding file.

        This method reverses the space escaping performed by `process_token_text_for_txt_file`.

        Args:
            text (str): The text to unescape.

        Returns:
            str: The unescaped text.
        """

        if text:
            return text.replace("!"," ") # unescape to get back the space
        else:
            return ""




    def separate_punctuation(sentence):
        """
        Separates specified punctuation characters with a space before them.

        This helps in tokenization by treating punctuation as separate tokens.

        Args:
            sentence (str): The input sentence.

        Returns:
            str: The sentence with separated punctuation.
        """
        punctuation_regex = re.compile(r"([{}])".format(re.escape("".join(PUNCTUATION_TO_SEPARATE))))
        return punctuation_regex.sub(r" \1", sentence)

    
    def sentence_to_vec(self,sentence):
        """
        Generates a sentence embedding by averaging the word vectors of its constituent words.

        Args:
            sentence (str): The input sentence.

        Returns:
            list: A list representing the sentence embedding.
        """

        words = EmbeddingModel.separate_punctuation(sentence).lower().split()
        
        vectors = [self.dictionary[w] for w in words if w in self.dictionary]

        if vectors:
            return np.mean(vectors, axis=0).tolist()
        else:
            return np.zeros(self.vector_size).tolist()




    def __init__(self,model_path,unescape_words=False):

        """
        Initializes the WordEmbeddingModel by loading word vectors from a file.

        Args:
            model_path (str): The path to the word embedding file.
            unescape_words (bool): Whether to unescape words read from the file.
        """


        self.dictionary = {}
        self.vector_size = 0
        self.model_path = model_path

        with open(self.model_path, 'r', encoding='utf-8') as f:
            for line in f:
                values = line.split()
                if unescape_words:
                    word = EmbeddingModel.unescape_token_text_for_txt_file(values[0])
                else:
                    word = values[0]
                vector = np.asarray(values[1:], "float32")
                self.dictionary[word] = vector
                if self.vector_size==0:
                    self.vector_size = len(vector)




    def open_file(modelPath):
        """Opens a file, handling gzip compression if necessary.

        Args:
            modelPath: Path to the file.

        Returns:
            A file object.
        """
        try:
            # Try opening as gzip first
            f = gzip.open(modelPath, 'rt', encoding='utf-8')
            # If successful, return the gzip file object
            # Try reading a line to check if it's a valid gzip
            f.readline()
            # If successful, reset file pointer and return the gzip file object
            f.seek(0)
            return f
        except gzip.BadGzipFile:
            # If not a gzip, open as a regular file
            f = open(modelPath, 'r', encoding='utf-8')
            # Return the regular file object
            return f


    #This method will generate an embedding for a piece of text
    def sentence_to_vec(self,sentence):

        words = sentence.lower().split()
        
        vectors = [self.dictionary[w] for w in words if w in self.dictionary]

        if vectors:
            return np.mean(vectors, axis=0).tolist()
        else:
            return np.zeros(self.vector_size).tolist()
