from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

with open("docs/knowledge.txt", "r") as f:
    text = f.read()

documents = [Document(page_content=text)]

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

db = FAISS.from_documents(docs, embeddings)

db.save_local("vectorstore")

print("Vector database created successfully")
