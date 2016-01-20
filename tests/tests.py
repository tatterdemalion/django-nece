#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .models import Fruit
from .fixtures import create_fixtures
from nece.exceptions import NonTranslatableFieldError


class TranslationTest(TestCase):
    def setUp(self):
        create_fixtures()

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

    def test_nontranslatable_fields(self):
        fruit = Fruit.objects.get(name='apple')
        with self.assertRaises(NonTranslatableFieldError) as error:
            fruit.translate('it_it', dummy_field='hello')
        self.assertEqual(error.exception.fieldname, 'dummy_field')

    def test_translation_mapping(self):
        self.assertTrue(Fruit.objects.language('tr').exists())
        self.assertEqual(Fruit.objects.language('tr')[0].name, 'elma')
