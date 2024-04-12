from langchain.text_splitter import RecursiveCharacterTextSplitter

# import tiktoken


class Spliter:
    def splitter_text(self, data):
        # text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        text_splitter = RecursiveCharacterTextSplitter(
            # chunk_size=256, chunk_overlap=64
        )
        all_splits = text_splitter.split_documents(data)

        # print(all_splits)

        return all_splits
