from bs4 import BeautifulSoup
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
import requests

RESULTS_PER_QUESTION = 3
ddg_search = DuckDuckGoSearchAPIWrapper()
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

def web_search(query: str, num_results: int = RESULTS_PER_QUESTION):
    results = ddg_search.results(query, num_results)
    return [r["link"] for r in results]
