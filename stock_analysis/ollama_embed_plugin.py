from langchain_community.embeddings import OllamaEmbeddings

class OllamaPlugin():
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

o = OllamaPlugin()