# from document_ingestion import ingest_document

# if __name__ == "__main__":
#     doc_path = "data/raw_docs/sample_concert.txt"
#     result = ingest_document(doc_path)
#     print(result)

# from qa_service import answer_question

# if __name__ == "__main__":
#     query = "Where is Lady Gaga performing in autumn 2025?"
#     response = answer_question(query)
#     print("💬 Answer:", response)
from utils import print_faiss_contents

print_faiss_contents()
