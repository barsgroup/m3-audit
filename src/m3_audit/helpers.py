#coding: utf-8
"""
Вспомогательные методы модуля
-----------------------------

.. Created on 29.10.11
.. @author: ruldashev
"""
from __future__ import absolute_import
from collections import OrderedDict

from django.db.models.base import ModelBase
from django import forms as form_fields
# TODO: collections.OrderedDict не подойдет?
from django.utils.datastructures import OrderedDict

from m3.ui.ext import fields as ext_fields
from m3.ui.ext.misc import store


def fields_for_model(model, fields=None, exclude=None, widgets=None, formfield_callback=None):
    u"""Возвращает словарь, содержащий поля модели. В отличии от
    :py:meth:`django.forms.models.fields_for_model` вытаскивает также non editable поля

    :param model: модель приложения
    :type model: :py:class:`django.db.models.model`
    :param fields: указанные филды добавятся в результат
    :type fields: list
    :param exclude: указанные филды исключатся из результата
    :type fields: list
    """
    field_list = []
    ignored = []
    opts = model._meta
    for f in opts.fields + opts.many_to_many:
        # TODO: обязательно проверять на None
        if fields is not None and not f.name in fields:
            continue
        if exclude and f.name in exclude:
            continue
        if widgets and f.name in widgets:
            kwargs = {'widget': widgets[f.name]}
        else:
            kwargs = {}

        # TODO: обязательно проверять на None
        if formfield_callback is None:
            formfield = f.formfield(**kwargs)
        elif not callable(formfield_callback):
            raise TypeError('formfield_callback must be a function or callable')
        else:
            formfield = formfield_callback(f, **kwargs)

        if formfield:
            field_list.append((f.name, formfield))
        else:
            ignored.append(f.name)
    field_dict = OrderedDict(field_list)
    if fields:
        field_dict = OrderedDict(
            [(f, field_dict.get(f)) for f in fields
                if ((not exclude) or (exclude and f not in exclude)) and (f not in ignored)]
        )
    return field_dict


# TODO: такое объявление списка не желательно, насколько помнится
def ext_fields_for_model(model, exclusion=[]):
    u"""
    Возвращает список, содержащий поля модели в виде ExtFields.

    :param model: модель приложения
    :type model: :py:class:`django.db.models.model`
    :param exclusion: указанные филды исключатся из результата
    :type exclusion: list
    """
    assert isinstance(model, ModelBase)
    model_ext_fields = {}
    
    # маппер Django Forms Fields -> ExtFields
    # TODO: использовать общий маппер (если/когда он будет)
    # TODO: не лучше создавать словарь сразу заполненным
    mapper = dict()
    default_field = ext_fields.ExtStringField
    mapper[form_fields.IntegerField] = ext_fields.ExtNumberField
    mapper[form_fields.Textarea] = ext_fields.ExtTextArea
    mapper[form_fields.DateTimeInput] = ext_fields.ExtDateField
    mapper[form_fields.Select] = ext_fields.ExtComboBox

    fields = list(fields_for_model(model).items())
    for key, field in fields:
        if key in exclusion:
            continue
        
        field_cls = field.widget.__class__
        ext_field = mapper[field_cls]() if field_cls in mapper else default_field()

        ext_field.name = key
        ext_field.label = field.label
        if hasattr(field, 'choices'):
            # если есть список, значит построим комбобокс
            ext_field.set_store(store.ExtDataStore(data=field.choices))
            ext_field.display_field = 'name'
            ext_field.value_field = 'id'
            ext_field.trigger_action = 'all'

        model_ext_fields[key] = ext_field
        
    return model_ext_fields