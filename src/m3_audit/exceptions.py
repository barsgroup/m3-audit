#coding:utf-8
u"""
Исключения системы
-------------------

.. Created on 22.12.2010

.. @author: akvarats
"""


class M3AuditException(Exception):
    u"""
    Некоторое исключение подсистемы аудита
    """
    pass


class DropM3AuditCacheException(M3AuditException):
    u"""
    Исключение, которое возникает при попытке сброса кеша, хранящего
    зарегистрированные типы аудита
    """
    pass


class NoWriteMethonInM3AuditException(M3AuditException):
    u"""
    Выбрасывается в случае, если при регистрации аудита у класса модели
    не найден 
    """
    pass