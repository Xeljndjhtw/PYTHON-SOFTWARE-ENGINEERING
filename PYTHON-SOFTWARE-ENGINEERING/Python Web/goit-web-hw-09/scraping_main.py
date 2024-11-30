from scrapy.crawler import CrawlerProcess
from scrapy import Spider
from scrapy.utils.project import get_project_settings
import json

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com"]

    def parse(self, response):
        # Обробка кожної цитати на сторінці
        for quote in response.css("div.quote"):
            author_url = quote.css("span a::attr(href)").get()
            yield {
                'quote': quote.css("span.text::text").get().strip(),  # Текст цитати
                'author': quote.css("span small.author::text").get().strip(),  # Ім'я автора
                'tags': quote.css("div.tags a.tag::text").getall(),  # Теги цитати
                'author_url': response.urljoin(author_url) if author_url else None  # URL сторінки автора
            }

        # Перевірка наявності посилання на наступну сторінку
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)  # Перехід до наступної сторінки

class AuthorSpider(Spider):
    name = "authors"
    custom_settings = {
        'ITEM_PIPELINES': {
            '__main__.AuthorPipeline': 1
        }
    }

    def __init__(self, author_urls):
        self.start_urls = author_urls

    def parse(self, response):
        # Обробка сторінки автора
        yield {
            'fullname': response.css("h3.author-title::text").get().strip(),  # Повне ім'я автора
            'born_date': response.css("span.author-born-date::text").get().strip(),  # Дата народження
            'born_location': response.css("span.author-born-location::text").get().strip(),  # Місце народження
            'description': " ".join(response.css("div.author-description::text").getall()).strip()  # Опис автора
        }

class AuthorPipeline:
    def open_spider(self, spider):
        self.file = open("authors.json", "w", encoding="utf-8")  # Відкриття файлу для збереження даних про авторів

    def close_spider(self, spider):
        self.file.close()  # Закриття файлу після завершення роботи

    def process_item(self, item, spider):
        self.file.write(json.dumps(item, ensure_ascii=False) + "\n")  # Запис даних у файл
        return item

if __name__ == "__main__":
    # Краулінг цитат
    process = CrawlerProcess(get_project_settings())

    process.crawl(QuotesSpider)
    process.start()

    # Завантаження URL сторінок авторів
    author_urls = []
    with open("quotes.json", "r", encoding="utf-8") as f:
        quotes = json.load(f)
        for quote in quotes:
            if quote['author_url'] and quote['author_url'] not in author_urls:
                author_urls.append(quote['author_url'])

    # Краулінг авторів
    process.crawl(AuthorSpider, author_urls=author_urls)
    process.start()
