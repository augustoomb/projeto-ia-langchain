from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

import os


class Store:
    def create_llm(self, key):
        os.environ["OPENAI_API_KEY"] = key

    def save_to_store(self, all_splits, data_folder_name):
        if self.check_store(data_folder_name):
            self.save_to_existing_store(all_splits, data_folder_name)
        else:
            self.create_store(all_splits, data_folder_name)

    def check_store(self, data_folder_name):
        return os.path.isdir(f"./data/{data_folder_name}/vector_store")

    # SALVANDO NUM BANCO DE DADOS VETORIAL
    def create_store(self, all_splits, data_folder_name):
        vectorstore = Chroma.from_documents(
            documents=all_splits,  # indexa os documentos para permitir buscas rápidas posteriormente
            embedding=OpenAIEmbeddings(),
            persist_directory=f"./data/{data_folder_name}/vector_store",
        )

        vectorstore.persist()

    def save_to_existing_store(self, all_splits, data_folder_name):
        vector_store = Chroma(
            persist_directory=f"./data/{data_folder_name}/vector_store",
            embedding_function=OpenAIEmbeddings(),
        )

        vector_store.add_documents(all_splits)
        vector_store.persist()
