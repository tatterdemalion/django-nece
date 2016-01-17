# -*- coding: utf-8 -*-
from django import forms
from django.forms import Widget
from django import utils
import copy
import json
from django.forms.utils import flatatt


class TranslationWidget(forms.Widget):
    """
    forked from https://github.com/abbasovalex/django-SplitJSONWidget-form
    """
    def __init__(self, attrs=None, instance=None):
        self.newline = '<br/>'
        self.separator = '__'
        self.instance = instance
        self.translatable_fields = instance.translatable_fields
        Widget.__init__(self, attrs)

    def _as_text_field(self, name, key, value, is_sub=False):
        attrs = self.build_attrs(self.attrs, type='text',
                                 name="%s%s%s" % (name, self.separator, key))
        attrs['value'] = utils.encoding.force_unicode(value)
        attrs['id'] = attrs.get('name', None)
        return u""" <label for="%s">%s:</label>
        <input%s />""" % (attrs['id'], key, flatatt(attrs))

    def _to_build(self, name, json_obj, hierarchy=0, fields_left=[]):
        inputs = []

        def get_input_list(title):
            if not hierarchy:
                return []
            return ['%s:%s' % (title, self.newline)]

        def add_to_input_list(input_list, name, key, value):
            input_list.append(
                self._to_build(
                    "%s%s%s" % (name, self.separator, key), value,
                    hierarchy=hierarchy + 1))

        if isinstance(json_obj, list):
            title = name.rpartition(self.separator)[2]
            input_list = get_input_list(title)
            for key, value in enumerate(json_obj):
                add_to_input_list(input_list, name, key, value)
            inputs.extend([input_list])
        elif isinstance(json_obj, dict):
            title = name.rpartition(self.separator)[2]
            input_list = get_input_list(title)
            if hierarchy == 1:
                for key in self.translatable_fields:
                    value = json_obj.get(key, '')
                    add_to_input_list(input_list, name, key, value)
            else:
                for key, value in json_obj.items():
                    add_to_input_list(input_list, name, key, value)
            inputs.extend([input_list])
        elif isinstance(json_obj, (basestring, int, float)):
            name, _, key = name.rpartition(self.separator)
            inputs.append(self._as_text_field(name, key, json_obj))
        elif json_obj is None:
            name, _, key = name.rpartition(self.separator)
            inputs.append(self._as_text_field(name, key, ''))
        return inputs

    def _prepare_as_ul(self, inputs, hierarchy=0):
        if inputs:
            result = ''
            for el in inputs:
                if isinstance(el, list) and len(inputs) == 1:
                    result += '%s' % self._prepare_as_ul(
                        el, hierarchy=hierarchy + 1)
                elif isinstance(el, list):
                    result += '<ul>'
                    result += '%s' % self._prepare_as_ul(
                        el, hierarchy=hierarchy + 1)
                    result += '</ul>'
                else:
                    result += '<li>%s</li>' % el
                if hierarchy == 0:
                    result += '<ul><li><a href="#">add language</a></li></ul>'
            return result
        return ''

    def _to_pack_up(self, root_node, raw_data):

        copy_raw_data = copy.deepcopy(raw_data)
        result = []

        def _to_parse_key(k, v):
            if k.find(self.separator) != -1:
                apx, _, nk = k.rpartition(self.separator)
                try:
                    # parse list
                    int(nk)
                    l = []
                    obj = {}
                    index = None
                    if apx != root_node:
                        for key, val in copy_raw_data.items():
                            head, _, t = key.rpartition(self.separator)
                            _, _, index = head.rpartition(self.separator)
                            if key is k:
                                del copy_raw_data[key]
                            elif key.startswith(apx):
                                try:
                                    int(t)
                                    l.append(val)
                                except ValueError:
                                    if index in obj:
                                        obj[index].update({t: val})
                                    else:
                                        obj[index] = {t: val}
                                del copy_raw_data[key]
                        if obj:
                            for i in obj:
                                l.append(obj[i])
                    l.append(v)
                    return _to_parse_key(apx, l)
                except ValueError:
                    # parse dict
                    d = {}
                    if apx != root_node:
                        for key, val in copy_raw_data.items():
                            _, _, t = key.rpartition(self.separator)
                            try:
                                int(t)
                                continue
                            except ValueError:
                                pass
                            if key is k:
                                del copy_raw_data[key]
                            elif key.startswith(apx):
                                d.update({t: val})
                                del copy_raw_data[key]
                    v = {nk: v}
                    if d:
                        v.update(d)
                    return _to_parse_key(apx, v)
            else:
                return v
        for k, v in raw_data.iteritems():
            if k in copy_raw_data:
                # to transform value from list to string
                v = v[0] if isinstance(v, list) and len(v) is 1 else v
                if k.find(self.separator) != -1:
                    d = _to_parse_key(k, v)
                    # set type result
                    if not len(result):
                        result = type(d)()
                    try:
                        result.extend(d)
                    except:
                        result.update(d)
        return result

    def value_from_datadict(self, data, files, name):
        data_copy = copy.deepcopy(data)
        result = self._to_pack_up(name, data_copy)
        return json.dumps(result)

    def render(self, name, value, attrs=None):
        try:
            value = json.loads(value)
        except (TypeError, KeyError):
            pass
        inputs = self._to_build(name, value or {}, hierarchy=0)
        result = self._prepare_as_ul(inputs)
        return utils.safestring.mark_safe(result)
