from typing import List

from ..models import Author
from ..validators.validators import AuthorInput


class AuthorService:
    def __init__(self, AuthorModel):
        self.Author = AuthorModel

    def get_or_create_authors(self, authors_data: List[AuthorInput]) -> List[Author]:
        authors = []
        for data in authors_data:
            if not data.first_name and not data.last_name:
                continue
            author_obj, _ = self.Author.objects.get_or_create(
                first_name=data.first_name,
                last_name=data.last_name,
                bio=data.bio,
            )
            authors.append(author_obj)
        return authors
