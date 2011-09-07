#coding:utf-8
'''

Описание менеджера, который обслуживает систему аудита

Created on 21.12.2010

@author: akvarats
'''

from django.db import transaction

from m3.helpers import logger
from m3.data.caching import RuntimeCache

from exceptions import (DropM3AuditCacheException, 
                        NoWriteMethonInM3AuditException)


__all__=('AuditManager',)


class AuditCache(RuntimeCache):
    '''
    Кеш с информацией о зарегистрированных типах аудита
    '''
    def drop(self, dimensions):
        raise DropM3AuditCacheException()
    
    def drop_all(self):
        raise DropM3AuditCacheException()
    
    

class AuditManager(object):
    '''
    Менеджер, который выполняет запись результатов аудита
    '''
    
    def register(self, audit_name, audit_model):
        '''
        Регистрирует тип аудита
        '''
        
        if not hasattr(audit_model, 'write'):
            raise NoWriteMethonInM3AuditException(audit_model.__module__ + '.' + audit_model.__name__)
        
        AuditCache().set(audit_name, audit_model)
        
    def get(self, audit_name, default=None):
        '''
        Возвращает данные, хранящиеся для аудита с указанным именем.
        
        Если аудит не найден, возвращается значение параметра default. 
        '''
        return AuditCache().get(audit_name, default)
    
    @transaction.commit_on_success
    def write(self, audit_name, user, *args, **kwargs):
        '''
        Выполняет операцию записи об аудите в базу данных
        '''
        audit = self.get(audit_name, None)
        if audit:
            try:
                audit.write(user, *args, **kwargs)
            except:
                logger.exception(u'Не удалось записать результаты аудита \'%s\'' % audit_name)
