from ..models import Publisher


class PublisherService:
    def __init__(self, PublisherModel):
        self.Publisher = PublisherModel

    def get_or_create_publisher(self, name: str) -> Publisher:
        publisher, _ = self.Publisher.objects.get_or_create(name=name)
        return publisher
