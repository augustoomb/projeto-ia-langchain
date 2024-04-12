import nest_asyncio

from langchain.document_loaders.sitemap import SitemapLoader

from langchain.document_loaders.pdf import PyMuPDFLoader

from utils import remove_nav_and_header_elements

# from langchain.document_loaders import WebBaseLoader

from langchain.document_loaders import TextLoader

nest_asyncio.apply()

import os
import re


class Loader:
    # CRIAR UM TIPO DEPOIS ??
    def get_loader_funcion(self):
        return {
            "pdf_loader": self.pdf_loader,
            "xml_sitemap": self.sitemap_loader,
            "text_loader": self.text_loader,
        }

    def create_loader(self, content_loader, data_folder_name):
        func_loader = self.get_loader_funcion()[content_loader["type_loader"]]
        # del func_loader["type_loader"]

        return func_loader(content_loader, data_folder_name)

    def sitemap_loader(self, content, _data_folder_name):
        xml_sitemap = content["xml_sitemap"]
        useful_urls = content["useful_urls"]

        sitemap_loader = SitemapLoader(
            web_path=xml_sitemap,
            filter_urls=useful_urls,
            parsing_function=remove_nav_and_header_elements,
        )

        sitemap_loader.requests_per_second = 4

        data = sitemap_loader.load()

        # company_folder_path = os.path.join("./data/conversations", company)
        company_folder_path = f"./assistants_openai/"

        if not os.path.exists(company_folder_path):
            os.makedirs(company_folder_path)

        # Caminho completo do arquivo
        file_path = os.path.join(company_folder_path, "contato_assistant.txt")

        # ESCREVER NO ARQUIVO
        # with open(file_path, "a") as file:
        #     file.write(formatted_data)

        with open(file_path, "a") as f:
            for doc in data:
                content = doc.page_content
                content = content.replace(". ", ".\n")
                content = content.replace("? ", "?\n")
                f.write(content)
                f.write("\n\n")

        return "OK"

    def pdf_loader(self, content, data_folder_name):
        pdf_file_name = content["pdf_file_name"]
        # loader = PyPDFLoader(f"./data/{data_folder_name}/files/pdf/{pdf_file_name}")
        loader = PyMuPDFLoader(f"./data/{data_folder_name}/files/pdf/{pdf_file_name}")
        data = loader.load()

        return data

    def text_loader(self, content, data_folder_name):
        text_file_name = content["text_file_name"]
        loader = TextLoader(f"./data/{data_folder_name}/files/txt/{text_file_name}")
        data = loader.load()

        return data
