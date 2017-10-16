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
                "fr_fr": {
                    "benefits": "bon pour la santé",
                    "name": "pomme"
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
        {
            "translations": {
                "fi_fi": {
                    "benefits": "Päärynät tarjoavat erittäin hyvä kuidun"
                    "lähde, ja ne ovat myös hyvä lähde B2-vitamiinia, "
                    "C, E, kupari, ja kalium.",
                    "name": "päärynät"
                },
                "tr_tr": {
                    "benefits": "Armut lif çok iyi bir kaynağı sağlar ve "
                    "aynı zamanda vitamin B2, C, E, bakır ve potasyum "
                    "için iyi bir kaynaktır.",
                    "name": "armut"
                }
            },
            "name": "pear",
            "benefits": "Pears provide a very good source of fiber and "
            "are also a good source of vitamin B2, C, E, copper, "
            "and potassium.",
            "scientific_name": "Pyrus"
        },
        {
            "name": "banana",
            "benefits": "Potassium",
            "scientific_name": "Musa acuminata"
        },

    ]
    n = n or len(fixtures)
    fixtures = itertools.cycle(fixtures)
    for _ in range(n):
        yield next(fixtures)


def create_fixtures(n=None):
    Fruit.objects.bulk_create(Fruit(**fruit) for fruit in get_fixtures(n))
