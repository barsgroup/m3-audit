#coding:utf-8
'''
Created on 22.12.2010

@author: akvarats
'''

class M3AuditException(Exception):
    '''
    Некоторое исключение подсистемы аудита
    '''
    pass

class DropM3AuditCacheException(M3AuditException):
    '''
    Исключение, которое возникает при попытке сброса кеша, хранящего
    зарегистрированные типы аудита
    '''
    pass

class NoWriteMethonInM3AuditException(M3AuditException):
    '''
    Выбрасывается в случае, если при регистрации аудита у класса модели
    не найден 
    '''
    pass