.. image:: https://img.shields.io/travis/tatterdemalion/django-nece/master.svg
    :target: https://travis-ci.org/tatterdemalion/django-nece

.. image:: https://img.shields.io/coveralls/tatterdemalion/django-nece.svg
    :target: https://coveralls.io/r/tatterdemalion/django-nece

.. image:: https://img.shields.io/pypi/v/nece.svg
    :target: https://pypi.python.org/pypi/nece

.. image:: https://img.shields.io/pypi/pyversions/nece.svg
    :target: https://pypi.python.org/pypi/nece/


nece?
=====

Introduction
------------

.. figure:: https://raw.githubusercontent.com/tatterdemalion/django-nece/master/images/nece.png
   :alt: nece

A “Content Translation Framework” using Postgresql’s jsonb field. It
simply sets and gets translations from a jsonb field called
``translations``.

Why?
~~~~

You might ask why you should use django-nece since there are other, and
more mature content translation frameworks like `django-hvad`_ and
`django-modeltranslation`_. Both of them are good in some ways, worst in
others.

For instance, it is very hard for ``django-hvad`` users to get default
language if there is no corresponding translation for an object. And it
holds translated values in a different table, so every translation query
results in another hit to the database.

On the other hand ``django-modeltranslation`` adds multiple additional
fields for multiple languages. The number of fields inceases by the
number of languages you need to support. At the end it becomes a huge
chunk of an object if you need to add more than 20 languages.

``nece?`` more or less works like the latter one with an important
difference. It uses Postgresql’s new ``JSONB`` field to hold translation
information. And overrides the original one on query.

Dependencies
------------

::

    postgresql >= 9.4.5
    Django >= 1.9
    psycopg2 >= 2.5.4


Installation
------------

via pypi:
~~~~~~~~~

::

    pip install nece

via setup.py
~~~~~~~~~~~~

::

    python setup.py install

Usage
-----

Lets say we have a model called ``Fruit``:

::

    from nece.models import TranslationModel

    class Fruit(TranslationModel):
        name = CharField(max_length=255)

        def __str__(self):
            return self.name
      
        class Meta:
            translatable_fields = ('name',)

``TranslationModel`` adds a jsonb field to this table and sets
translations in a notation like the one below:

::

    {u'de_de': {u'name': u'Apfel'},
     u'tr_tr': {u'name': u'elma'}}

When we need the German translation we can simply choose the language
and get the attribute as usual:

::

    >> f = Fruit.objects.get(name='apple')
    >> print(f.name)
    apple
    >> f.language('de_de')
    >> print(f.name)
    Apfel

You can also filter out the ones containing any language translation:

::

    >> Fruit.objects.all()
    [<Fruit: apple>, <Fruit: pear>, <Fruit: banana>]
    >> Fruit.objects.language('tr_tr')
    [<Fruit: elma>, <Fruit: armut>]  # there is no translation for banana
    >> Fruit.objects.language_or_default('tr_tr')
    [<Fruit: elma>, <Fruit: armut>, <Fruit: banana>]
    >> Fruit.objects.language('tr_tr').filter(name='elma')
    [<Fruit: elma>]
    >> Fruit.objects.language('tr_tr').get(name='elma')
    <Fruit: elma>

Updating translations
~~~~~~~~~~~~~~~~~~~~~

::

    >> fruit._language_code
    tr_tr
    >> fruit.name
    elma
    >> fruit.translate(name='armut').save()
    >> fruit.name
    armut
    >> fruit.language('en')
    >> fruit.translate('it_it', name='pera')
    >> fruit.language('it_it')
    >> fruit.name
    pera

Settings
--------

TRANSLATIONS_DEFAULT
~~~~~~~~~~~~~~~~~~~~

Default language code. Default value: ```en_us```

TRANSLATIONS_MAP
~~~~~~~~~~~~~~~~

Shortcuts for ```languagecode_countrycode``` notation. 

Example:

::

    TRANSLATIONS_MAP = {
        "en": "en_us",
        "tr": "tr_tr",
        "ar": "ar_sy",
        "bg": "bg_bg",
        "cs": "cs_cz",
        "da": "da_dk",
        ...
    }


Default:

::

    {'en': 'en_us'}



Contributors & Thanks
---------------------

- `Erkan Ay`_
- `Ayman Khalil`_
- `Gönül Sabah`_
- `Faruk Rahmet`_
- `Mathieu Richardoz`_
- `Marc Hertzog`_

`Change Log`_


.. _django-hvad: https://github.com/kristianoellegaard/django-hvad
.. _django-modeltranslation: https://github.com/deschler/django-modeltranslation
.. _Erkan Ay: https://github.com/erkanay
.. _Ayman Khalil: https://github.com/aymankh86
.. _Gönül Sabah: https://github.com/gonulsabah
.. _Faruk Rahmet: https://github.com/farukrahmet
.. _Mathieu Richardoz: https://github.com/metamatik
.. _Marc Hertzog: https://github.com/kemar
.. _Change Log: https://github.com/tatterdemalion/django-nece/blob/master/CHANGELOG.md
