import requests
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import api_keys

template = """

Summarize the following question based on the context:

Question: {question}

Context: {context}

"""

prompt = ChatPromptTemplate.from_template(template)

question = 'test'
print(template)
# llm = ChatOpenAI(api_key=api_keys.open_ai)
# response = llm.invoke("how can langsmith help with testing?")
# print(response)

def scrape_text(url: str):
    # Get the text of a page
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            page_text = soup.get_text(separator=" ", strip=True)

            return page_text
        else:
            return f"Failed to retrieve the webpage: Status code {response.status_code}"
    except Exception as e:
        print(e)
