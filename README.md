# django-nece

# Attention
 Please keep in mind that this app is under heavy development.

# Introduction
A translation mechanism using Postgresql's jsonb field. It simply sets and get translations from a jsonb field called ```translations```. 
It is a simple, yet powerful alternative to [django-hvad](https://github.com/KristianOellegaard/django-hvad). Here is how it works:

Lets say we have a model called ```Fruit```:
```
from nece.models import TranslationModel

class Fruit(TranslationModel):
    name = CharField(max_length=255)
    translatable_fields = ['name']

    def __str__(self):
        return self.name
```

```TranslationModel``` adds a jsonb field to this table and sets translations in a notation like the one below:

```
{u'de_de': {u'name': u'Apfel'},
 u'tr_tr': {u'name': u'elma'}}
```

When we need the German translation we can simply choose the language and get the attribute as usual:

```
>> f = Fruit.objects.get(name='apple')
>> print(f.name)
apple
>> f.language('de_de')
>> print(f.name)
Apfel
```

You can also filter out the ones containing any language translation:

```
>> Fruit.objects.all()
[<Fruit: apple>, <Fruit: pear>, <Fruit: banana>]
>> Fruit.objects.language('tr_tr')
[<Fruit: elma>, <Fruit: armut>]  # there is no translation for banana
>> Fruit.objects.language_or_default('tr_tr')
[<Fruit: elma>, <Fruit: armut>, <Fruit: banana>]
```

## Updating translations

```
>> fruit._language_code
tr_tr
>> fruit.name
elma
>> fruit.translate(name='armut').save()
>> fruit.name
armut
>> fruit.language('en')
>> fruit.name
apple
```

## Adding new languages

```
>> fruit.translate('it_it', name='mela')
>> fruit.language('it_it').name
mela
```

## what is nece?

It is Turkish for 'In what language?' or more literally something like 'whatish?' :)


