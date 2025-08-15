from apps.books.scrapers.piter_publ.book_parser import BookParser


class TestBookParser:
    def test_extract_book_name_success(self):
        """тест успешного извлечения названия книги"""
        html = """
        <div class="product-info">
            <h1>Python для начинающих</h1>
        </div>
        """
        parser = BookParser(html)
        result = parser.extract_book_name()

        assert result["book_title"] == "Python для начинающих"

    def test_extract_book_name_not_found(self):
        """тест когда название книги не найдено"""
        html = "<div>не заголовка</div>"
        parser = BookParser(html)
        result = parser.extract_book_name()
        assert result["book_title"] == ""

    def test_extract_book_name_exception(self, monkeypatch):
        """тест исключения при извлечении названия"""
        parser = BookParser('<div class="product-info"><h1>Test</h1></div>')

        # ломаем select_one чтобы вызвать исключение
        def broken_select_one(*args):
            raise Exception("Test error")

        monkeypatch.setattr(parser.soup, "select_one", broken_select_one)
        result = parser.extract_book_name()

        assert result["book_title"] == ""

    def test_extract_description_success(self):
        """тест извлечения описания"""
        html = '<div id="tab-1">Описание книги</div>'
        parser = BookParser(html)
        result = parser.extract_description()

        assert result["description"] == "Описание книги"

    def test_extract_description_not_found(self):
        """тест когда описание не найдено"""
        html = "<div>нет tab-1</div>"
        parser = BookParser(html)
        result = parser.extract_description()

        assert result["description"] == ""

    def test_extract_description_exception(self, monkeypatch):
        """тест исключения при извлечении описания"""
        parser = BookParser('<div id="tab-1">Test</div>')

        def broken_find(*args, **kwargs):
            raise Exception("Test error")

        monkeypatch.setattr(parser.soup, "find", broken_find)
        result = parser.extract_description()

        assert result["description"] == ""

    def test_extract_all_params(self):
        """тест извлечения всех параметров"""
        html = """
        <div class="params">
            <li><span class="grid-5">ISBN:</span>
                <span class="grid-7">978-1-2345</span></li>
            <li><span class="grid-5">Год:</span>
                <span class="grid-7">2024</span></li>
            <li><span class="grid-5">Страниц:</span>
                <span class="grid-7">350</span></li>
        </div>
        """
        parser = BookParser(html)
        result = parser.extract_all_params()

        assert result["ISBN"] == "978-1-2345"
        assert result["Год"] == "2024"
        assert result["Страниц"] == "350"

    def test_extract_cover_image(self):
        """тест извлечения обложки"""
        html = '<div class="photo"><img src="/images/cover.jpg"/></div>'
        parser = BookParser(html)
        result = parser.extract_cover_image()

        assert result["cover_image"].endswith("/images/cover.jpg")

    def test_extract_cover_image_not_found(self):
        """тест когда обложка не найдена"""
        html = "<div>нет картинки</div>"
        parser = BookParser(html)
        result = parser.extract_cover_image()

        assert result["cover_image"] == ""

    def test_extract_cover_image_fallback_to_any_img(self):
        """тест извлечения картинки без div.photo"""
        html = '<img src="/fallback.jpg"/>'
        parser = BookParser(html)
        result = parser.extract_cover_image()

        assert result["cover_image"].endswith("/fallback.jpg")

    def test_extract_cover_image_exception(self, monkeypatch):
        """тест исключения при извлечении обложки"""
        parser = BookParser('<div class="photo"><img src="/test.jpg"/></div>')

        def broken_select_one(*args):
            raise Exception("Test error")

        monkeypatch.setattr(parser.soup, "select_one", broken_select_one)
        result = parser.extract_cover_image()

        assert result == {"cover": ""}

    def test_extract_authors(self):
        """тест извлечения авторов"""
        html = """
        <div id="tab-2">
            <div class="autor-wrapper">
                <h2>Иван Иванов</h2>
                Биография автора
            </div>
        </div>
        """
        parser = BookParser(html)
        result = parser.extract_authors()

        assert len(result) == 1
        assert result[0]["last_name"] == "Иван"
        assert result[0]["first_name"] == "Иванов"

    def test_extract_authors_single_name(self):
        """тест автора с одним именем"""
        html = """
        <div id="tab-2">
            <div class="autor-wrapper">
                <h2>Пушкин</h2>
            </div>
        </div>
        """
        parser = BookParser(html)
        result = parser.extract_authors()

        assert result[0]["last_name"] == "Пушкин"
        assert result[0]["first_name"] == ""

    def test_extract_authors_three_or_more_names(self):
        """тест автора с тремя и более именами"""
        html = """
        <div id="tab-2">
            <div class="autor-wrapper">
                <h2>Александр Сергеевич Пушкин</h2>
            </div>
        </div>
        """
        parser = BookParser(html)
        result = parser.extract_authors()

        assert result[0]["first_name"] == "Сергеевич"
        assert result[0]["last_name"] == "Александр Пушкин"

    def test_extract_authors_empty_name(self):
        """тест автора с пустым именем"""
        html = """
        <div id="tab-2">
            <div class="autor-wrapper">
                <h2></h2>
            </div>
        </div>
        """
        parser = BookParser(html)
        result = parser.extract_authors()

        assert result[0]["first_name"] == ""
        assert result[0]["last_name"] == ""

    def test_extract_authors_exception(self, monkeypatch):
        """тест исключения при извлечении авторов"""
        parser = BookParser(
            '<div id="tab-2"><div class="autor-wrapper"><h2>Test</h2></div></div>'
        )

        def broken_select(*args):
            raise Exception("Test error")

        monkeypatch.setattr(parser.soup, "select", broken_select)
        result = parser.extract_authors()

        assert result == []

    def test_extract_author_bio_success(self):
        """тест извлечения биографии автора"""
        html = """
        <div class="author-wrapper">
            <div class="grid-9 s-grid-12">
                <h2>Иван Иванов</h2>
                Биография автора тут
            </div>
        </div>
        """
        parser = BookParser(html)
        result = parser.extract_author_bio()

        assert "Биография автора тут" in result

    def test_extract_author_bio_not_found(self):
        """тест когда биография не найдена"""
        html = "<div>нет биографии</div>"
        parser = BookParser(html)
        result = parser.extract_author_bio()

        assert result == ""

    def test_extract_author_bio_exception(self, monkeypatch):
        """тест исключения при извлечении биографии"""
        parser = BookParser(
            '<div class="author-wrapper"><div class="grid-9 s-grid-12"><h2>Test</h2></div></div>'
        )

        def broken_select_one(*args):
            raise Exception("Test error")

        monkeypatch.setattr(parser.soup, "select_one", broken_select_one)
        result = parser.extract_author_bio()

        assert result == {"author_bio": ""}

    def test_extract_price(self):
        """тест извлечения цены"""
        html = """
        <div class="price color">1000 ₽</div>
        <div class="price color">500 ₽</div>
        """
        parser = BookParser(html)
        result = parser.extract_price()

        assert result["price"] == "1000 ₽"
        assert result["electronic_price"] == "500 ₽"

    def test_extract_price_less_than_two_prices(self):
        """тест когда цен меньше двух"""
        html = '<div class="price color">1000 ₽</div>'
        parser = BookParser(html)
        result = parser.extract_price()

        assert result == {}

    def test_extract_price_exception(self, monkeypatch):
        """тест исключения при извлечении цены"""
        parser = BookParser('<div class="price color">100</div>')

        def broken_select(*args):
            raise Exception("Test error")

        monkeypatch.setattr(parser.soup, "select", broken_select)
        result = parser.extract_price()

        assert result == {"price": "", "electronic_price": ""}
