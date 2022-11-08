from django.test import TestCase
from .utils import populate_cards_by_address, test_dict


class NYCAccessibleStreetsTests(TestCase):
    def populate_cards_test(self):
        test_dict()
        populate_cards_by_address()
