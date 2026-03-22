from langchain_ollama import ChatOllama

class Model():
    def __init__(self,system =''):
        self.llm = ChatOllama(model = 'llama3.2',url='http://127.0.0.1:11434')
        self.system = system

    def invoke(self,content):
        response = self.llm.invoke([
        {"role": "system", "content": self.system},
        {"role": "user", "content": content}
    ])
        return response.content
    