from gpt_index import SimpleDirectoryReader, LLMPredictor
from gpt_index.indices.knowledge_graph.base import GPTKnowledgeGraphIndex
from langchain import OpenAI
from IPython.display import Markdown, display

from pyvis.network import Network

llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-002"))
new_index = GPTKnowledgeGraphIndex.load_from_disk('index_kg.json', llm_predictor=llm_predictor)

g = new_index.get_networkx_graph()
net = Network(notebook=False, cdn_resources="in_line", directed=True)
net.from_nx(g)
net.show("example_2048_8.html")