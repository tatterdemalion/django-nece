#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from nece_test.models import Fruit


class TranslationTest(TestCase):
    def setUp(self):
        fruit = Fruit.objects.create(name='apple', benefits='good for health')
        fruit.translate('de_de', name='Apfel',
                        benefits='gut für die Feuerstelle')
        fruit.translate('tr_tr', name='elma', benefits='Kalbe yararlıdır')
        fruit.save()

    def test_query(self):
        self.assertTrue(Fruit.objects.all())

    def test_language_filter(self):
        self.assertEqual(Fruit.objects.language('de_de')[0].name, 'Apfel')

    def test_language_switch(self):
        fruit = Fruit.objects.get(name='apple')
        self.assertEqual(fruit.name, 'apple')
        fruit.language('tr_tr')
        self.assertEqual(fruit.name, 'elma')
        self.assertEqual(fruit.default_language.name, 'apple')
        fruit.language('de_de')
        self.assertEqual(fruit.name, 'Apfel')
        self.assertEqual(fruit.default_language.name, 'apple')

    def test_save_correct_languages(self):
        fruit = Fruit.objects.get(name='apple')
        fruit.translate(name='not apple')
        fruit.language('tr_tr')
        fruit.translate(name='elma değil')
        self.assertEqual(fruit.translations['tr_tr']['name'], 'elma değil')
        fruit.language('de_de')
        fruit.translate(name='nicht Apfel')
        self.assertEqual(fruit.translations['de_de']['name'], 'nicht Apfel')
        self.assertEqual(fruit.default_language.name, 'not apple')
        fruit.save()
