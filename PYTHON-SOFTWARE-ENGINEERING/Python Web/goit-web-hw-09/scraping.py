import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"

# Функція для отримання цитат із сторінки
def scrape_quotes(page_url):
    quotes_data = []
    authors_data = {}

    while page_url:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser")

        quotes = soup.select(".quote")
        for quote in quotes:
            text = quote.select_one(".text").get_text(strip=True)
            author_name = quote.select_one(".author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.select(".tag")]

            # Зберігаємо цитати
            quotes_data.append({
                "tags": tags,
                "author": author_name,
                "quote": text
            })

            # Зберігаємо інформацію про автора, якщо її ще немає
            if author_name not in authors_data:
                author_url = BASE_URL + quote.select_one(".author + a")["href"]
                authors_data[author_name] = scrape_author(author_url)

        # Перевірка наявності наступної сторінки
        next_page = soup.select_one(".next > a")
        page_url = BASE_URL + next_page["href"] if next_page else None

    return quotes_data, authors_data

# Функція для отримання інформації про автора
def scrape_author(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, "html.parser")

    fullname = soup.select_one(".author-title").get_text(strip=True)
    born_date = soup.select_one(".author-born-date").get_text(strip=True)
    born_location = soup.select_one(".author-born-location").get_text(strip=True)
    description = soup.select_one(".author-description").get_text(strip=True)

    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }

if __name__ == "__main__":
    # Початкова сторінка
    start_url = BASE_URL

    # Скрапінг даних
    quotes, authors = scrape_quotes(start_url)

    # Збереження в JSON файли
    with open("quotes.json", "w", encoding="utf-8") as quotes_file:
        json.dump(quotes, quotes_file, ensure_ascii=False, indent=4)

    with open("authors.json", "w", encoding="utf-8") as authors_file:
        json.dump(list(authors.values()), authors_file, ensure_ascii=False, indent=4)

    print("Скрапінг завершено. Дані збережено у файли quotes.json та authors.json.")
