from ingest import load_faqs, build_index
from rag_helper import RAGBase


document = load_faqs()
index = build_index(document)
rag = RAGBase(index)

print(rag.rag("Is there a certificate?", "machine-learning-zoomcamp"))  