import requests
from minsearch import Index

def load_faqs():
    docs_url = "https://datatalks.club/faq/json/courses.json"
    courses = requests.get(docs_url).json()
    prefix_url = "https://datatalks.club/faq/"

    raw_docs = []
    for course in courses:
        url = f"{prefix_url}{course['path']}"
        course_response = requests.get(url)
        course_response.raise_for_status()
        course_data = course_response.json()
        
        raw_docs.extend(course_data)
        
    documents = []
    for doc in raw_docs:
        documents.append({
            "course": doc['course'],
            'section': doc['section'],
            'question': doc['question'],
            'answer': doc['answer']
                        })
    return documents


def build_index(documents):
    index = Index(
        text_fields = ['question', 'answer', 'section'],
        keyword_fields = ['course']
    )
    index.fit(documents)
    return index