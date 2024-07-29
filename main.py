import requests
import api_keys
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

template = """

Summarize the following question based on the context:

Question: {question}

Context: {context}

"""


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

prompt = ChatPromptTemplate.from_template(template)

url = "https://blog.langchain.dev/announcing-langsmith"
pageContent = scrape_text(url)
chain = prompt | ChatOpenAI(model="gpt-3.5-turbo-1106") | StrOutputParser()

response = chain.invoke(
    {
        "question": "what is langsmith",
        "context": pageContent
    }
)

print(response)