import os
from flask import Flask, request

from Chat import Chat
from utils import get_links, send_message_zap, decode_jwt, file_uploader
from Loader import Loader
from Spliter import Spliter
from Store import Store

# import pathlib

# import json


app = Flask(__name__)


@app.route("/")
def teste():
    return "Rota de teste"


@app.route("/file-upload", methods=["POST"])
def file_upload():
    try:
        user_token = request.headers.get("user-token")
        user = decode_jwt(user_token)
        company = user["company"]

        files = request.files.getlist("files")
        filetype = request.form.get("filetype")

        if not files or not type:
            raise Exception("Os parâmetros files e filetype devem ser informados")

        file_uploader(filetype, files, company)

        return {"message": f"Arquivo {filetype} enviado com sucesso!"}

    except Exception as e:
        message = f"Ocorreu um erro: {e}"
        # logging.error(message)
        return {"message": message}, 400


@app.route("/send-whatsapp", methods=["POST"])
def send_message_to_whatsapp():
    try:
        # QUANDO O WEBHOOK TWILIO FUNCIONAR, AQUI DEVO CONSEGUIR PUXAR
        # O NÚMERO DO CLIENTE (BUSCAR NO QUE VIER COMO REQUEST)
        # QUANDO CONSEGUIR, AJUSTAR/TROCAR NO "destination"
        req_json = request.get_json()
        account_sid = req_json["account_sid"]
        auth_token = req_json["auth_token"]
        message = req_json["message"]
        destination = req_json["destination"]

        send_message_zap(account_sid, auth_token, message, destination)

        return {"message": "Mensagem enviada com sucesso"}

    except KeyError as e:
        message = f"Um ou mais parâmetros não foram informados corretamente: {str(e)}"
        # logging.error(message)
        # return {"message": message}, 400
        return {"message": message}, 400

    except Exception as e:
        message = f"Ocorreu um erro: {e}"
        # logging.error(message)
        return {"message": message}, 400


@app.route("/generate-links", methods=["POST"])
def generate_links():
    try:
        req_json = request.get_json()
        xml_sitemap = req_json["xml_sitemap"]
        terms_to_exclude = req_json["terms_to_exclude"]

        links = get_links(xml_sitemap, terms_to_exclude)

        return {"links": links}

    except KeyError as e:
        message = f"Um ou mais parâmetros não foram informados corretamente: {str(e)}"
        # logging.error(message)
        # return {"message": message}, 400
        return {"message": message}, 400

    except Exception as e:
        message = f"Ocorreu um erro: {e}"
        # logging.error(message)
        return {"message": message}, 400


# RODAR APENAS UMA VEZ. VAI CRIAR O ARQUIVO DE DADOS DO CLIENTE
@app.route("/create-data", methods=["POST"])
def document_loader():
    try:
        # DADOS PASSADOS POR PARÂMETRO
        # key = request.headers.get("key")
        user_token = request.headers.get("user-token")
        user = decode_jwt(user_token)
        key = user["key_openai"]

        req_json = request.get_json()
        data_folder_name = req_json["data_folder_name"]
        content = req_json["content"]

        # RASPANDO urls_uteis INFORMADAS
        loader = Loader()
        loader.create_loader(content, data_folder_name)

        # # QUEBRANDO O CONTEÚDO EM PARTES
        # spliter = Spliter()
        # all_splits = spliter.splitter_text(data)

        # # SALVANDO NUM BANCO DE DADOS VETORIAL
        # store = Store()
        # store.create_llm(key)
        # # store.create_store(all_splits, data_folder_name)
        # store.save_to_store(all_splits, data_folder_name)

        return {"status": "Dados da empresa foram criados e salvos com sucesso"}

    except KeyError as e:
        message = f"Um ou mais parâmetros não foram informados corretamente: {str(e)}"
        # logging.error(message)
        # return {"message": message}, 400
        return {"message": message}, 400

    except Exception as e:
        message = f"Ocorreu um erro: {str(e)}"
        # logging.error(message)
        return {"message": message}, 400


@app.route("/create-user", methods=["POST"])
def create_user():
    pass

    # ENTRADA:
    ## RECEBE UM TOKEN JWT (USER, PASS E TOKEN OPENAI)
    ## CRIAR O USER COM TUDO ISSO NO BANCO

    # RESPOSTA:
    ## OK


@app.route("/qa", methods=["POST"])
# @cache.cached()
def qa():
    try:
        user_token = request.headers.get("user-token")
        req_json = request.get_json()
        question = req_json["question"]
        chat_id = req_json.get("chat_id", 0)

        user = decode_jwt(user_token)

        chat = Chat()

        if not chat.check_store(user["company"]):
            # raise Exception("A pasta com dados da sua empresa não está cadastrada")
            return {
                "message": "A pasta com dados da sua empresa não está cadastrada"
            }, 404
        else:
            chat.create_llm(user["key_openai"])
            chat.load_store(user["company"])
            # chat.create_memory()
            chat.create_chat()
            response = chat.question_and_answer(question, user["company"], chat_id)
            chat.close_chat()
            del chat
            return response

    except KeyError as e:
        message = f"Um ou mais parâmetros não foram informados corretamente: {str(e)}"
        # logging.error(message)
        return {"message": message}, 400

    except Exception as e:
        message = f"Ocorreu um erro: {e}"
        # logging.error(message)
        return {"message": message}, 400


@app.route("/close", methods=["DELETE"])
def close():
    pass
    # try:
    #     global chat
    #     if chat is None:
    #         return {"message": "Não há chat ativo"}
    #     else:
    #         chat.close_chat()
    #         chat = None
    #         return {"message": "Chat encerrado"}

    # except Exception as e:
    #     message = f"Ocorreu um erro: {e}"
    #     # logging.error(message)
    #     return {"message": message}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
