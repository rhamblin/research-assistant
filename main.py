import api_keys
from web_scraper_utils import web_search, scrape_text
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda

template = """{text}

--------------

Using the above text, answer in short the following question:

> {question}

--------------
if the question cannot be answered using the text, imply summarize the text. Include all factual information , numbers stats etc
"""

prompt = ChatPromptTemplate.from_template(template)

url = "https://blog.langchain.dev/announcing-langsmith"
pageContent = scrape_text(url)
scrape_and_summarize_chain = RunnablePassthrough.assign(
    text=lambda x: scrape_text(x["url"])[:10000]
) | prompt | ChatOpenAI(model="gpt-3.5-turbo-1106") | StrOutputParser()

chain = RunnablePassthrough.assign(
    urls=lambda x: web_search(x["question"])
) | (lambda x: [{"question": x["question"], "url": u} for u in x["urls"]]) | scrape_and_summarize_chain.map()

response = chain.invoke(
    {
        "question": "what is langsmith"
    }
)

print(response)