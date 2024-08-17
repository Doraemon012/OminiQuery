import os
import pickle
import faiss
import numpy as np
from sqlalchemy import create_engine

SCHEMA_CACHE_DB_URI = f'sqlite:///schemadb.db'
schema_cache_engine = create_engine(SCHEMA_CACHE_DB_URI)

# class FaissStore
class FaissStore:

    def __init__(self, dir: str, name: str, cohere_client):
        self.name = name
        self.co = cohere_client
        if not os.path.exists(dir):
            os.makedirs(dir)

        self.store_file = os.path.join(dir, f"{name}.pkl")
        self.index_file = os.path.join(dir, f"{name}.index")

        if not (os.path.exists(self.index_file) and os.path.exists(self.store_file)):
            self.store = None
        else:
            with open(self.store_file, "rb") as f:
                self.store = pickle.load(f)
            self.store['index'] = faiss.read_index(self.index_file)

    def _persist(self):
        faiss.write_index(self.store['index'], self.index_file)
        index = self.store['index']
        self.store['index'] = None
        with open(self.store_file, "wb") as f:
            pickle.dump(self.store, f)
        self.store['index'] = index

    def write(self, schemas: dict):
        """
        The function writes all table schemas into long-term memory by embedding the texts and storing
        them along with the schemas.
        
        :param schemas: The `schemas` parameter is a dictionary containing table schemas where the keys
        are the names of the tables and the values are the schema definitions for each table. This
        function takes these table schemas, converts them into text representations, embeds them using a
        specified model, and then stores the embeddings along with the
        :type schemas: dict
        """
        """Batch writing all table schemas into long-term memory."""
        
        texts = list(schemas.keys())
        response = self.co.embed(texts=texts, model='embed-english-light-v3.0', input_type="search_document")

        embeddings = np.array(response.embeddings)

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        self.store = {'index': index, 'texts': texts, 'schemas': schemas}
        self._persist()

    def search(self, query, k=10):
        """
        This function searches for the top k tables that are most related to a given query using
        embeddings and a stored index.
        
        :param query: The `query` parameter in the `search` method is the text input that you want to
        search for in the tables. It is the query string that you want to find the most relevant tables
        for
        :param k: The parameter `k` in the `search` method specifies the number of top tables that are
        most related to the query that should be returned. It determines how many results will be
        retrieved and presented to the user. In this case, the default value for `k` is set to 10,,
        defaults to 10 (optional)
        :return: a list of the top k tables that are most related to the query. The tables are retrieved
        based on their relevance to the query, as determined by the stored index.
        """
        """Search top k tables that most relate to the query."""
        if not self.store:
            print("No store found. Please write schemas first.")
            return []

        # embeddings of query
        query_emb = self.co.embed(texts=[query], input_type="search_query", model="embed-english-light-v3.0").embeddings
        query_emb = np.asarray(query_emb)

        # use stored index to search
        D, I = self.store['index'].search(query_emb, k)

        # return the most relevant tables in order
        return [self.store['texts'][idx] for idx in I[0]]
        # return [self.store['texts'][idx] for idx in I[0]]