# nece?

# Attention
 Please keep in mind that **nece** is under heavy development.

# Introduction


![nece](https://raw.githubusercontent.com/tatterdemalion/django-nece/master/images/nece.png)

A "Content Translation Framework" using Postgresql's jsonb field. It simply sets and gets translations from a jsonb field called ```translations```. 
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

## Admin Integration

**nece** has an out-of-the box admin integration by default. It is not pretty yet. But it is also not that hard to use a generic JSON widget.

![admin](https://raw.githubusercontent.com/tatterdemalion/django-nece/master/images/admin.png)


## Why?

You might ask why should you use django-nece since there are other, and more mature content translation frameworks like [django-hvad](https://github.com/kristianoellegaard/django-hvad) and [django-modeltransltaion](https://github.com/deschler/django-modeltranslation). Both of them are good in some ways, worst in others. 

For instance, it is very hard for ```django-hvad``` users to get default language if there is no corresponding translation for an object. And it holds translated values in a different table, so every translation query results in another hit to the database.

On the other hand ```django-modeldtranslations``` adds multiple additional fields for multiple languages. The number of fields inceases by the number of languages you need to support. At the end it becomes a huge chunk of an object if you need to add more than 20 languages.

```nece?``` more or less works like the latter one with an important difference. It uses Postgresql's new ```JSONB``` field to hold translation information. And overrides the original one on query.

