#coding:utf-8
u"""
m3_audit.manager
----------------

Описание менеджера, который обслуживает систему аудита

Created on 21.12.2010

@author: akvarats
"""

from django.db import transaction

from m3.helpers import logger
from m3.data.caching import RuntimeCache

from exceptions import (DropM3AuditCacheException, 
                        NoWriteMethonInM3AuditException)


__all__=('AuditManager',)


class AuditCache(RuntimeCache):
    u"""
    Кеш с информацией о зарегистрированных типах аудита
    """
    def drop(self, dimensions):
        raise DropM3AuditCacheException()
    
    def drop_all(self):
        raise DropM3AuditCacheException()
    
    

class AuditManager(object):
    u"""
    Менеджер, который выполняет запись результатов аудита
    """
    
    def register(self, audit_name, audit_model):
        u"""
        Регистрирует тип аудита

        :param audit_name: название аудита
        :type audit_name: str
        :param audit_model: модель аудита
        :type audit_model: :py:class:`django.db.models.model`
        """
        
        if not hasattr(audit_model, 'write'):
            raise NoWriteMethonInM3AuditException(audit_model.__module__ + '.' + audit_model.__name__)
        
        AuditCache().set(audit_name, audit_model)

    def list(self):
        u"""
        Возвращает список зарегистрированных аудитов
        """
        return [x[0] for x in AuditCache().data]
        
    def get(self, audit_name, default=None):
        u"""
        Возвращает данные аудита

        :param audit_name: название аудита
        :type audit_name: str
        :param default: значение, если аудит не найден в кеше
        :type default: str
        """
        return AuditCache().get(audit_name, default)
    
    @transaction.commit_on_success
    def write(self, audit_name, user, *args, **kwargs):
        u"""
        Выполняет операцию записи об аудите в базу данных

        :param audit_name: название аудита
        :type audit_name: str
        :param user: пользователь системы
        """
        audit = self.get(audit_name, None)
        if audit:
            try:
                audit.write(user, *args, **kwargs)
            except:
                logger.exception(u'Не удалось записать результаты аудита \'%s\'' % audit_name)
