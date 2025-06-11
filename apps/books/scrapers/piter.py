import asyncio
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from base import BaseScraper


class PiterScraper(BaseScraper):
    """
    парсит ссылки на книги по каждой странице
    """

    BASE_URL = "https://www.piter.com/collection/all?q=python"

    async def scrape_book_links(self, url):
        current_url = url
        book_links = []
        page_number = 1

        while current_url:
            print(f"\n load page {page_number}: {current_url}")
            html = await self.fetch(current_url)
            soup = self.parse(html)

            try:
                link_tags = soup.find("div", class_="products-list").find_all("a")
                found_on_page = 0

                for link in link_tags:
                    href = link.get("href")
                    if href and href.startswith("/collection/all/product/"):
                        full_url = urljoin("https://www.piter.com/", href)
                        book_links.append(full_url)
                        found_on_page += 1
                print(f"✅ links found: {found_on_page} (total: {len(book_links)})")

                if found_on_page == 0:
                    print("no books found on page. End of extraction")
                    break

            except AttributeError as e:
                print(f"failed to find products list: {e}")
                print(f"page HTML: {html[:500]}...")
                break

            next_button = soup.find("a", string="Следующая")
            if next_button and next_button.get("href"):
                print(f"➡️ going to next page: {next_button}")
                href = next_button["href"]
                full_url = urljoin("https://www.piter.com/", href)
                match = re.search(r"page=(\d+)", href)
                if match:
                    page = int(match.group(1))
                    current_url = full_url
                    page_number = page
                    await asyncio.sleep(1)
                    response = await self.fetch(current_url)
                    html = response
                else:
                    print("no valid page number in next link. End of extraction")
                    break

            else:
                print("no valid page number in next link. End of extraction")
                break

        print(f"\n total book links found: {len(book_links)}. Finished extraction")
        if book_links:
            print((f"first 5 links: {book_links[:5]}"))
        return book_links


class BookParser:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "lxml")

    def extract_author(self):
        tag = self.soup.select_one("p.author a")
        return {"name": tag.get_text(strip=True), "url": tag["href"]} if tag else {}

    def extract_price(self):
        tags = self.soup.select("div.price.color")
        if len(tags) >= 2:
            return {
                "price": tags[0].text.strip(),
                "electronic_price": tags[1].text.strip(),
            }
        return {}

    def extract_details(self):
        info = {}
        for li in self.soup.select("ul.clear-list li.clearfix"):
            key = li.find("span", class_="grid-5")
            value = li.find("span", class_="grid-7")
            if key and value:
                info[key.text.strip().rstrip(":")] = value.text.strip()
        return info


class LinksList(BaseScraper):
    """
    принимает список ссылок на книги, отправляет их для парсинга в BookParser
    """

    def __init__(self, delay: float = 1.0):
        super().__init__(delay)

    async def scrape_books(self, links: list[str]) -> list[dict]:
        books = []

        for link in links:
            print(f"🔍 parsing book: {link}")
            html = await self.fetch(link)
            if not html:
                print(f"skipped due to fetch error: {link}")
                continue

            parser = BookParser(html)
            book_data = {
                "url": link,
                "author": parser.extract_author(),
                "price": parser.extract_price(),
                "details": parser.extract_details(),
            }
            books.append(book_data)
            del html
        print(f"\n total books parsed: {len(books)}")
        return books


# url = 'https://www.piter.com/collection/all?q=python'
# scraper = PiterScraper()
# result = asyncio.run(scraper.scrape_book_links(url))
# print(result)


async def main():
    piter = PiterScraper()
    links = await piter.scrape_book_links(PiterScraper.BASE_URL)

    book_scraper = LinksList(delay=1.0)
    books = await book_scraper.scrape_books(links)

    print(f"\n📘 parsed {len(books)} books")
    for book in books[:3]:
        print(book)


if __name__ == "__main__":
    asyncio.run(main())
