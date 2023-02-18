from gpt_index import SimpleDirectoryReader, LLMPredictor
from gpt_index.indices.knowledge_graph.base import GPTKnowledgeGraphIndex
from langchain import OpenAI
from IPython.display import Markdown, display

documents = SimpleDirectoryReader('./data').load_data()

# define LLM
# NOTE: at the time of demo, text-davinci-002 did not have rate-limit errors
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-002"))

# NOTE: can take a while! 
index = GPTKnowledgeGraphIndex(
    documents, 
    chunk_size_limit=2048, 
    max_triplets_per_chunk=8,
    llm_predictor=llm_predictor
)

index.save_to_disk('index_kg.json')