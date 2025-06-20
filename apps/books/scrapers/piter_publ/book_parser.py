from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin

from logger.logger import setup_logger

logger = setup_logger(module_name=__name__, log_dir="logs/scrapers")


class BookParser:
    def __init__(self, html: str, base_domain: str = "https://www.piter.com"):
        self.soup = BeautifulSoup(html, "lxml")
        self.base_domain = base_domain

    def extract_book_name(self):
        try:
            title = self.soup.select_one("div.product-info h1")
            if not title:
                logger.warning("book title not found in HTML")
                return {"book_title": ""}

            result = {"book_title": title.get_text(strip=True) if title else ""}
            logger.debug(f"extracted book title: {result['book_title']}")
            return result
        except Exception as e:
            logger.error(f"book title extraction failed {str(e)}")
            return {"book_title": ""}

    def extract_description(self):
        try:
            description = self.soup.find("div", id="tab-1")
            if not description:
                logger.warning("book description not found in HTML")
                return {"description": ""}
            full_text = description.get_text(separator="\n", strip=True)
            logger.debug(f"extracted book description: {full_text}")
            return {"description": full_text}
        except Exception as e:
            logger.error(f"description extraction failed {str(e)}")
            return {"description": ""}

    def extract_all_params(self):
        result = {}
        items = self.soup.select("div.params li")

        for li in items:
            label = li.select_one("span.grid-5")
            value = li.select_one("span.grid-7")
            if label and value:
                key = label.get_text(strip=True).rstrip(":")
                val = value.get_text(strip=True)
                result[key] = val
        return result

    def extract_cover_image(self):
        try:
            container = self.soup.select_one('div.photo, div[class*="photo"]')
            if container:
                img = container.select_one("img")
                if img and img.get("src"):
                    src = img["src"].strip()
                    logger.debug(f"extracted cover image from container: {src}")
                    return {"cover_image": urljoin("https://www.piter.com", src)}

            img = self.soup.select_one("img")
            if img and img.get("src"):
                src = img["src"].strip()
                logger.debug(f"extracted cover image from img: {src}")
                return {"cover_image": urljoin("https://www.piter.com", src)}

            return {"cover_image": ""}
        except Exception as e:
            logger.error(f"cover extraction failed {str(e)}")
            return {"cover": ""}

    def extract_authors(self) -> List[Dict[str, str]]:
        try:
            authors = []
            author_blocks = self.soup.select("#tab-2 .autor-wrapper")

            for block in author_blocks:
                name_tag = block.select_one("h2")
                if name_tag:
                    full_name = name_tag.get_text(strip=True)
                    parts = full_name.split()
                    if len(parts) == 2:
                        last_name, first_name = parts
                    elif len(parts) == 3:
                        last_name = " ".join(parts[:-1])
                        first_name = parts[-1]
                    else:
                        logger.warning(
                            f"unusual author name format in tab-2: {full_name}"
                        )
                        last_name = full_name
                        first_name = ""

                    authors.append(
                        {
                            "first_name": first_name.strip("."),
                            "last_name": last_name,
                        }
                    )

            logger.info(f"parsed {len(authors)} authors from tab-2")
            return authors
        except Exception as e:
            logger.error(f"failed to parse authors from tab-2: {str(e)}")
            logger.exception("tab-2 author parsing error details")
            return []

    def extract_author_bio(self) -> str:
        try:
            block = self.soup.select_one("div.author-wrapper div.grid-9.s-grid-12")
            if not block:
                logger.warning("block with author_bio not found in HTML")
                return ""
            name_tag = block.select_one("h2")
            name_text = name_tag.get_text(strip=True) if name_tag else ""
            full_text = block.get_text(separator=" ", strip=True)
            logger.debug(f"extracted author_bio: {full_text}")
            return full_text.replace(name_text, "", 1).strip()
        except Exception as e:
            logger.error(f"author_bio extraction failed {str(e)}")
            return {"author_bio": ""}

    def extract_price(self):
        try:
            price = self.soup.select("div.price.color")
            if len(price) >= 2:
                logger.debug(f"extracted price: {price}")
                return {
                    "price": price[0].text.strip(),
                    "electronic_price": price[1].text.strip(),
                }
            return {}
        except Exception as e:
            logger.error(f"price extraction failed {str(e)}")
            return {"price": "", "electronic_price": ""}
