#coding:utf-8
u"""
Основные модели аудита
----------------------

.. Created on 17.12.2010

.. @author: akvarats
"""

from __future__ import absolute_import
from django.db import models
from django.core import serializers
from django.contrib.auth.models import User, AnonymousUser

from m3.db import BaseObjectModel
from .manager import AuditManager


class BaseAuditModel(BaseObjectModel):
    u"""
    Базовая модель, от которой наследуются все 
    модели хранения результатов аудита
    """
    
    # данные пользователя. специально не делается ForeignKey.
    # чтобы не быть завязанными на ссылочную целостность
    # * логин пользователя в системе (на момент записи значения
    username = models.CharField(u'Логин пользователя', max_length=50, null=True, blank=True,
                                db_index=True, default=u'')
    
    # * идентификатор пользователя
    userid = models.PositiveIntegerField(u'Идентификатор пользователя',
                                         default=0, db_index=True)

    # * ФИО пользователя на момент записи значения (для ускоренного отображения 
    #   значений
    user_fio = models.CharField(u'ФИО пользователя', max_length=70, null=True, blank=True,
                                db_index=True, default=u'')
    
    # * дополнительные сведения о пользователе (например, сотрудником какого 
    #   учреждения он являлся на момент записи
    user_info = models.CharField(u'Дополнительные сведения о пользователе',
                                 max_length=200, null=True, blank=True, default=u'')
    
    # серверный таймстамп на запись аудита
    created = models.DateTimeField(u'Дата создания', auto_now_add=True, db_index=True)


    # список отображаемых колонок (формат - как в диктах)
    list_columns = [
        ('username', u'Пользователь'),
        ('user_info', u'Доп. инфо'),
        ('created', u'Дата'),
    ]

    # список отображаемых полей в детализации.
    # По умолчанию - все из модели аудита
    list_fields = []

    class Meta:
        abstract = True
        
    def by_user(self, user):
        u"""
        Заполняет значения полей моделей на основе переданного пользователя

        :param user: пользователь
        :type user: :py:class:`django.db.models.Models`
        """
        # TODO: может лучше проверять user.is_anonymous()
        if isinstance(user, User):
            self.username = user.username
            self.userid = user.id  
            self.user_fio = (user.first_name + ' ' + user.last_name).strip()
        elif isinstance(user, AnonymousUser):
            self.username = 'anonymous'
            self.userid = 0
            self.user_fio = u'<Анонимный пользователь>'

    
class BaseModelChangeAuditModel(BaseAuditModel):
    u"""
    Аудит, предназначенный для отслеживания изменений в моделях системы
    """
    
    #===========================================================================
    # Типы операций над моделью
    #===========================================================================
    ADD = 0
    EDIT = 1
    DELETE = 2
    
    # Данные модели, для которой был выполнен аудит
    # * идентификатор объекта (специально не храним FK, чтобы была возможность
    #   безболезненно удалять объекты
    object_id = models.PositiveIntegerField(u'ID записи', default=0, db_index=True)
    object_model = models.CharField(u'Модель', max_length=300, db_index=True)
    # данные модели, на момент записи аудита
    object_data = models.TextField(u'Данные модели')
    
    type = models.PositiveIntegerField(u'Действие',
                                       choices=((ADD, u'Добавление'),
                                                (EDIT, u'Изменение'),
                                                (DELETE, u'Удаление'),),
                                       db_index=True)

    list_columns = [
        ('username', u'Пользователь'),
        ('object_id', u'ID записи', 30),
        ('object_model', u'Модель'),
        ('type', u'Действие', 70),
        ('created', u'Дата'),
    ]

    # TODO: переименовать type, чтобы не перекрывал стандартный объект type
    @classmethod
    def write(cls, user, model_object, type, *args, **kwargs):
        u"""
        Сохранение аудита

        :param user: пользоватьель
        :type user: :py:class:`django.contrib.auth.models.User`
        :param model_object: модель системы
        :type model_object: :py:class:`django.db.models.Models`
        :param type: тип действия (добавление, удаление, редактирование)
        """
        
        audit = cls()
        audit.by_user(user)
        
        if (type == BaseModelChangeAuditModel.ADD or 
            type == 'add' or type == 'new'):
            audit.type = BaseModelChangeAuditModel.ADD
            
        elif (type == BaseModelChangeAuditModel.EDIT or
              type == 'edit'):
            audit.type = BaseModelChangeAuditModel.EDIT
            
        elif (type == BaseModelChangeAuditModel.DELETE or
              type == 'remove' or
              type == 'delete'):
            audit.type = BaseModelChangeAuditModel.DELETE

        # TODO: model_object.id or 0 красивей
        audit.object_id = model_object.id if model_object.id else 0
        audit.object_model = (model_object.__class__.__module__ + 
                              '.' + 
                              model_object.__class__.__name__)
        try:
            audit.object_data = serializers.serialize('json', [model_object,])
        except:
            # TODO: лучше залогировать ошибку
            pass
        audit.save()
    
    class Meta:
        abstract = True


#===============================================================================
# Общий аудит для сохранения информации об изменении моделей
#===============================================================================
class DefaultModelChangeAuditModel(BaseModelChangeAuditModel):
    u"""
    Модель аудита, регистрирует изменения таблиц системы
    """
    
    class Meta:
        verbose_name = u'Изменения таблиц системы'
        db_table = 'm3_audit_model_changes'
        
AuditManager().register('model-changes', DefaultModelChangeAuditModel)


#===============================================================================
# Аудит для сохранения информации об изменении записей справочников
#===============================================================================
class DictChangesAuditModel(BaseModelChangeAuditModel):
    u"""
    Модель аудита, регистрирует изменения в справочниках
    """
    
    class Meta:
        verbose_name = u'Изменения в справочниках'
        db_table = 'm3_audit_dict_changes'

AuditManager().register('dict-changes', DictChangesAuditModel)


#===============================================================================
# Преднастроенный аудит для входов/выходов пользователей из системы
#===============================================================================
class AuthAuditModel(BaseAuditModel):
    u"""
    Модель аудита, регистрирует входы/выходы пользователя из системы
    """
    #===========================================================================
    # Тип авторизации пользователя
    #===========================================================================
    LOGIN = 0
    LOGOUT = 1
    
    type = models.PositiveIntegerField(u'Действие',
                                       choices=((LOGIN, u'Вход в систему'),
                                                (LOGOUT, u'Выход из системы'),), 
                                       db_index=True)

    list_columns = [
        ('userid', u'ID', 30),
        ('username', u'Пользователь'),
        ('type', u'Действие'),
        ('created', u'Дата'),
    ]

    # TODO: переименовать type, чтобы не перекрывал стандартный объект type
    @classmethod
    def write(cls, user, type='login', *args, **kwargs):
        u"""
        Сохранение аудита

        :param user: пользоватьель
        :type user: :py:class:`django.contrib.auth.models.User`
        :param type: тип действия (авторизация, выход)
        """
        audit = AuthAuditModel()
        audit.by_user(user)
        audit.type = AuthAuditModel.LOGIN if type == 'login' else AuthAuditModel.LOGOUT
        audit.save()
    
    class Meta:
        verbose_name = u'Авторизации пользователей'
        db_table = 'm3_audit_auth'

AuditManager().register('auth', AuthAuditModel)


## Структура данных аудита по действиям над ролями пользователей
class RolesAuditModel(BaseAuditModel):
    u"""
    Модель аудита, регистрирует изменения ролей пользователей
    """
    PERMISSION_ADDITION = 0
    PERMISSION_REMOVAL = 1
    PERMISSION_ENABLEMENT = 2
    PERMISSION_DISABLEMENT = 3
    
    type = models.PositiveIntegerField(u'Действие',
                                       choices=((PERMISSION_ADDITION, u'Добавление прав'),
                                                (PERMISSION_REMOVAL, u'Лишение прав'),
                                                (PERMISSION_ENABLEMENT, u'Активация права'),
                                                (PERMISSION_DISABLEMENT, u'Отключение права')
                                                ))
    role_id = models.PositiveIntegerField(u'ID роли')
    role_name = models.CharField(u'Роль', max_length=200)
    permission_code = models.CharField(u'Разрешения', max_length=200,
                                       null=True, blank=True, default='')

    list_columns = [
        ('username', u'Пользователь'),
        ('role_id', u'ID роли', 30),
        ('role_name', u'Роль'),
        ('type', u'Действие', 70),
        ('created', u'Дата'),
    ]

    # TODO: переименовать type, чтобы не перекрывал стандартный объект type
    @classmethod
    def write(cls, user, role, permission_or_code=None, type=PERMISSION_ADDITION,
              *args, **kwargs):
        u"""
        Сохранение аудита

        :param user: пользоватьель
        :type user: :py:class:`django.contrib.auth.models.User`
        :param role: роль
        :param permission_or_code: разрешения
        :param type: действие (добавление, лишение, активация, отключение)
        """
        audit = RolesAuditModel()
        audit.by_user(user)
        
        audit.type = type
        audit.role = role
        audit.permission_code = cls.parse_permission(permission_or_code)
        audit.save()
    
    def get_role(self):
        return RolesAuditModel.objects.get(self.role_id)

    def set_role(self, role):
        self.role_id = role.id
        self.role_name = role.name

    role = property(get_role, set_role)
    
    @classmethod
    def parse_permission(cls, perm):
        u"""
        Возвращает разрешение

        :param perm: разрешение
        """
        permission_code = perm; return permission_code
    
    class Meta:
        verbose_name = u'Изменения ролей пользователей'
        db_table = 'm3_audit_roles' 
        
AuditManager().register('roles', RolesAuditModel)