#-*- coding: utf-8 -*-
import itertools

from .models import Fruit


def get_fixtures(n=None):
    fixtures = [
        {
            "translations": {
                "de_de": {
                    "benefits": "gut für die Feuerstelle",
                    "name": "Apfel"
                },
                "ku_tr": {
                    "name": "sêv"
                },
                "tr_tr": {
                    "benefits": "Kalbe yararlıdır",
                    "name": "elma"
                }
            },
            "name": "apple",
            "benefits": "good for health",
            "scientific_name": "malus domestica"
        },
    ]
    n = n or len(fixtures)
    fixtures = itertools.cycle(fixtures)
    for _ in xrange(n):
        yield next(fixtures)


def create_fixtures(n=None):
    Fruit.objects.bulk_create(Fruit(**fruit) for fruit in get_fixtures(n))
