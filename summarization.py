from langchain import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain

llm = OpenAI(temperature=0, max_tokens=600)

text_splitter = CharacterTextSplitter()

with open('ChatBot/test_output.txt') as f:
    state_of_the_union = f.read()
texts = text_splitter.split_text(state_of_the_union)

docs = [Document(page_content=t) for t in texts]

chain = load_summarize_chain(llm, chain_type="map_reduce")
print(chain.run(docs))