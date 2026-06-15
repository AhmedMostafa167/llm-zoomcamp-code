from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client = Groq()

INSTRUCTIONS = """
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
"""

PROMPT_TEMPLATE = """
QUESTION: {question}

CONTEXT:
{context}
""".strip()

class RAGBase:
    def __init__(
        self, 
        index, 
        client=client,
        instructions=INSTRUCTIONS,
        prompt_template=PROMPT_TEMPLATE,
        course="machine-learning-zoomcamp",
        model="llama-3.3-70b-versatile"
        ):
        self.index = index
        self.client = client
        self.instructions = instructions
        self.prompt_template = prompt_template
        self.course = course
        self.model = model
    
    def search_db(self, question, course):
        return self.index.search(
            question,
            boost_dict={"question": 2.0, 'section': 0.5},
            filter_dict={"course": course},
            num_results=5
            )
        
    def format_context(self, documents):
        context = []
        for doc in documents:
            context.append(f"""
            Question: {doc['question']}
            Answer: {doc['answer']}
            section: {doc['section']}
            """
            )
        return "\n\n".join(context)
        
    def build_prompt(self, question, context):
        return self.prompt_template.format(question=question, context=context)
    
    def llm(self, prompt):
        model = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", 
                "content": self.instructions},
                {"role": "user", "content": prompt},
            ],
        )
        return model.choices[0].message.content

    def rag(self, question, course):
        docs = self.search_db(question,course)
        context = self.format_context(docs)
        prompt = self.build_prompt(question, context)
        answer = self.llm(prompt)
        return answer
    
    

