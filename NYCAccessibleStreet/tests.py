from django.test import TestCase
from .utils import populate_cards_by_address


class NYCAccessibleStreetsTests(TestCase):
    def populate_cards_test(self):
        populate_cards_by_address()
