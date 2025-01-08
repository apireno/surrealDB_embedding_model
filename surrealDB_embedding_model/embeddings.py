import numpy as np
import gzip


class EmbeddingModel:


    def __init__(self,modelPath):
        self.dictionary = {}
        self.vector_size = 0
        with open(modelPath, 'r', encoding='utf-8') as f:
            for line in f:
                values = line.split()
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
