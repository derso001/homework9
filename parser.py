import requests
from bs4 import BeautifulSoup
import json

url = "https://quotes.toscrape.com/"

def save_data(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def parse(url):
    quotes = []
    author_info = []
    i = 0
    next_page = "/page/1/"

    while next_page:

        response = requests.get(url + next_page)
        soup = BeautifulSoup(response.text, "html.parser")

        for quote in soup.find_all("div", class_="quote"):
            quote_text = quote.find("span", class_="text").get_text()
            author_text = quote.find("small", class_="author").get_text()
            tags_list = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
            # [tag.get_text() for tag in quote_block.find_all("a", class_="tag")]

            quotes.append({
                "tags":tags_list,
                "author":author_text,
                "quote":quote_text
            })

            if author_text not in author_info:
                author_url = quote.find("a")["href"]
                author_response = requests.get(url + author_url)
                author_soup = BeautifulSoup(author_response.text, "html.parser")

                fullname_author = author_soup.find("h3", class_="author-title").get_text()
                born_date = author_soup.find("span", class_="author-born-date").get_text()
                born_location = author_soup.find("span", class_="author-born-location").get_text()
                description = author_soup.find("div", class_="author-description").get_text()

                author_info.append({
                    "fullname":fullname_author,
                    "born_date":born_date,
                    "born_location":born_location,
                    "description":description
                })

        print(f"done{i}")
        i += 1

        next_button = soup.find("li", class_="next")
        next_page = next_button.find("a")["href"] if next_button else None   

    return quotes, author_info 

if __name__ == "__main__":
    quotes, authors = parse(url)

    save_data(quotes, "data/quotes.json")
    save_data(authors, "data/authors.json")
        
