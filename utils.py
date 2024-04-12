from trafilatura import sitemaps
from twilio.rest import Client

import json
import jwt
import pickle
import uuid
import os
from langchain.schema.messages import ChatMessage
from typing import List
from bs4 import BeautifulSoup


# RECEBE UM LINK COM A HOME DO SITE OU UM SITEMAP(XML)
# DEVOLVE UM ARRAY DE LINKS, CONTENDO TODOS AS PÁGINAS DO SITE
def get_links(xml_sitemap, terms_to_exclude):
    links = sitemaps.sitemap_search(xml_sitemap)
    arr_filtrar = terms_to_exclude

    filtered_links = [l for l in links if all(termo not in l for termo in arr_filtrar)]
    # filtered_links = [l for l in links if "blog" not in l and "site-" not in l]
    return filtered_links


# -----------TWILIO
def send_message_zap(account_sid, auth_token, message, destination):
    client = Client(account_sid, auth_token)

    teste = client.messages.create(
        body=message,
        to=f"whatsapp:{destination}",
        from_="whatsapp:+14155238886",
    )

    print(teste)

    # client.messages.create(from_="whatsapp:+14155238886", to="whatsapp:+553188299510")


def id_generator():
    return str(uuid.uuid4())


def file_uploader(filetype, files, company):

    allowed_file_types = ["txt", "pdf"]
    if filetype not in allowed_file_types:
        raise Exception(
            f"Os tipos de arquivos permitidos são: {list(allowed_file_types)}"
        )

    company_folder_path = f"./data/{company}/files/{filetype}/"

    if not os.path.exists(company_folder_path):
        os.makedirs(company_folder_path)

    for file in files:
        if file.filename == "" or not file.filename.endswith(f".{filetype}"):
            raise Exception(f"O arquivo enviado não é um {filetype} válido")

        file.save(company_folder_path + file.filename)


# CONVERSAS
def escrever_no_arquivo(tuple, company, chat_id):
    try:
        # company_folder_path = os.path.join("./data/conversations", company)
        company_folder_path = f"./data/{company}/conversations"

        if not os.path.exists(company_folder_path):
            os.makedirs(company_folder_path)

        # Caminho completo do arquivo
        file_path = os.path.join(company_folder_path, f"{chat_id}.txt")

        # ESCREVER NO ARQUIVO
        with open(file_path, "a") as file:
            line = ", ".join(map(str, tuple)) + "\n"
            file.write(line)

    except FileNotFoundError:
        return ""


def ler_do_arquivo(company, chat_id):
    try:
        # file_path = os.path.join("./data/conversations", company, f"{chat_id}.txt")
        file_path = f"./data/{company}/conversations/{chat_id}.txt"
        arr_tuples = []

        with open(file_path, "r") as file:
            for line in file:
                # Converter a linha de volta para uma tupla
                tp = tuple(map(str.strip, line.split(",")))
                arr_tuples.append(tp)

        return arr_tuples

    except FileNotFoundError:
        return []


def decode_jwt(token, algorithms="HS256"):
    secret_key = ""
    # try:
    decoded_payload = jwt.decode(token, secret_key, algorithms=[algorithms])
    return decoded_payload
    # except jwt.ExpiredSignatureError:
    #     # Token expirado
    #     raise Exception("Token expirado")
    # except jwt.InvalidTokenError:
    #     # Token inválido
    #     raise Exception("Token inválido")


def remove_nav_and_header_elements(content: BeautifulSoup) -> str:
    # Find all 'nav', 'header', and 'form' elements in the BeautifulSoup object
    nav_elements = content.find_all("nav")
    header_elements = content.find_all("header")
    footer_elements = content.find_all("footer")
    form_elements = content.find_all("form")
    img_elements = content.find_all("img")
    link_elements = content.find_all("a")

    # Remove each 'nav', 'header', and 'form' element from the BeautifulSoup object
    for element in (
        nav_elements
        + header_elements
        + footer_elements
        + form_elements
        + img_elements
        + link_elements
    ):
        element.decompose()

    # Use get_text() with strip=True to get only the text content
    text_content = content.get_text(strip=True)
    return text_content


# FIM - LER E ESCREVER EM ARQUIVOS TEXTO COMUM


# SERIALIZADOS:


# def serialize_chat_messages(chat_messages: List[ChatMessage]):
#     return pickle.dumps(chat_messages)


# def deserialize_chat_messages(serialized_messages):
#     return pickle.loads(serialized_messages, encoding="utf-8")


# def save_chat_history_to_file(arr_chat_history):
#     serialized_messages = serialize_chat_messages(arr_chat_history)

#     # Caminho para o arquivo onde você deseja salvar os dados
#     caminho_arquivo_pickle = "dados.pkl"

#     # Escrevendo os dados serializados no arquivo
#     with open(caminho_arquivo_pickle, "wb") as arquivo:
#         arquivo.write(serialized_messages)


# def read_chat_history_in_file():
#     # Caminho para o arquivo onde os dados foram salvos
#     caminho_arquivo_pickle = "dados.pkl"
#     dados_lidos = None

#     # Lendo os dados do arquivo
#     with open(caminho_arquivo_pickle, "rb") as arquivo:
#         dados_lidos = pickle.load(arquivo)

#     return dados_lidos
