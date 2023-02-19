from langchain import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain

def summary(input_text):
    llm = OpenAI(temperature=0, max_tokens=600)

    text_splitter = CharacterTextSplitter()

    texts = text_splitter.split_text(input_text)

    docs = [Document(page_content=t) for t in texts]

    chain = load_summarize_chain(llm, chain_type="map_reduce")
    return chain.run(docs)