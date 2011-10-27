#coding:utf-8
'''
Created on 06.01.2011

@author: akvarats
'''
from m3.ui.actions import ActionPack, Action, utils, ControllerCache
from m3.helpers import urls
from m3.ui import actions

import ui
from manager import AuditManager

class BaseAuditUIActions(actions.ActionPack):
    '''
    Базовый пакет действий, который позволяет
    '''
    
    model = None
    acd = []

    # список отображаемых аудитов в комбо. По умолчанию - все
    list_audits = []

    # список отображаемых колонок (формат - как в диктах)
    list_columns = [
        ('username', u'Пользователь'),
        ('user_info', u'Доп. инфо'),
        ('created', u'Дата'),
    ]

    # список отображаемых полей в детализации.
    # По умолчанию - все из модели аудита
    list_fields = []
    
    def __init__(self):
        super(BaseAuditUIActions, self).__init__()

        self.list_window_action = BaseAuditListWindowAction()
        self.rows_action = AuditRowsDataAction()
        self.fields_action = AuditRowFieldsDataAction()
        self.list_sort_order = ['-created']
        
        self.actions.extend([self.rows_action,
                             self.list_window_action,
                             self.fields_action,
                             ])
    
    def get_acd(self):
        '''
        Возвращает context declaration на основе данных, прописанных
        при настройке дочернего класса
        '''
        if hasattr(self, 'acd'):
            return self.acd
    
    def get_list_window(self, window, request, context):
        '''
        Возвращает окно, в котором отображаются результаты аудита
        '''
        return window

    def get_list_url(self):
        '''
        Возвращает полный URL до действия на получение окна со списком
        записей аудита
        '''
        return self.list_window_action.absolute_url()

    def get_rows_url(self):
        '''
        Возвращает полный URL до действия на получение записей аудита
        '''
        return self.rows_action.absolute_url()

    def get_row_fields_url(self):
        '''
        Возвращает полный URL до действия на получение данных по записи аудита
        '''
        return self.fields_action.absolute_url()

    def configure_window(self, window, request, context):
        '''
        Конфигурация окна, выделено для возможности переопределения
        '''
        top_panel = self.get_top_panel(window, request, context)
        if top_panel:
            window.items.append(top_panel)
        
        east_panel = self.get_east_panel(window, request, context)
        if east_panel:
            window.items.append(east_panel)
        return window

    def get_east_panel(self, window, request, context):
        '''
        Возвращает панель с опциональными элементами формы,
        построенными по модели (list_fields)
        '''
        panel = ui.DefaultEastPanel()
        model = AuditManager().get(context.audit)
        panel.create_fields(model, self.list_fields)
        window.url_audit_row = self.get_row_fields_url()
        window.form_details = panel.form

        return panel

    def get_top_panel(self, window, request, context):
        '''
        Возвращает панель с опциональным списком для выбора аудита (list_audit)
        '''
        panel = ui.DefaultTopPanel()
        panel.create_audits_combo(context.audit, self.list_audits)
        window.url_audit_win = self.get_list_url()

        return panel

    def get_audits_config(self):
        """
        Собирает все экшенпаки аудитов в системе
        для использования их конфига list_columns и list_fields
        ЩИТО?
        """
        pass

    def get_rows(self, pre_query, request, context):
        '''
        '''
        return pre_query


class BaseAuditListWindowAction(actions.Action):
    '''
    Получение окна показа списка записей
    '''
    url = '/list-window'
    shortname = 'audit-list-window'

    def __init__(self, *args, **kwargs):
        super(BaseAuditListWindowAction, self).__init__(*args, **kwargs)

    def context_declaration(self):
        acd_list = self.parent.get_acd()
        acd_list.extend([actions.ACD(name='audit', type=str, required=True, default=''),])
        return acd_list

    def run(self, request, context):
        if not context.audit:
            # FIXME: какая-то нездоровая хуйня - достаем первый попавшийся аудит
            if self.parent.list_audits:
                context.audit = self.parent.list_audits[0]
            else:
                context.audit = AuditManager().list().keys()[0][0]

        window = ui.AuditListWindow()
        window = self.parent.get_list_window(window, request, context)
        
        window.grid_rows.url_data = self.parent.get_rows_url()
        window.create_columns(self.parent.list_columns)
        window = self.parent.configure_window(window, request, context)

        return actions.ExtUIScriptResult(data=window)


class AuditRowsDataAction(actions.Action):
    '''
    Действие на получение списка записей выбранного аудита
    '''
    url = '/rows'
    shortname = 'audit-rows'

    def context_declaration(self):
        acd_list = self.parent.get_acd()
        acd_list.extend([actions.ACD(name='audit', type=str, required=True),
                         actions.ACD(name='start', type=int, required=True, default=-1),
                         actions.ACD(name='limit', type=int, required=True, default=-1),])
        return acd_list

    def run(self, request, context):
        '''
        Выполняет построение предварительного запроса и отдает в функцию
        '''
        direction = request.REQUEST.get('dir')
        user_sort = request.REQUEST.get('sort')
        if direction == 'DESC':
            user_sort = '-' + user_sort
        sort_order = [user_sort] if user_sort else self.parent.list_sort_order
        
        model = AuditManager().get(context.audit)
        pre_query = model.objects.all()
        pre_query = utils.apply_sort_order(pre_query, self.parent.list_columns, sort_order)

        query = self.parent.get_rows(pre_query, request, context)

        return actions.ExtGridDataQueryResult(data=query,
                                              start=context.start,
                                              limit=context.limit)


class AuditRowFieldsDataAction(actions.Action):
    '''
    Действие на получение записи аудита
    '''
    url = '/row-fields'
    shortname = 'audit-row-fields'

    def context_declaration(self):
        acd_list = self.parent.get_acd()
        acd_list.extend([actions.ACD(name='audit', type=str, required=True),
                         actions.ACD(name='id', type=int, required=True, default=-1),])
        return acd_list

    def run(self, request, context):
        model = AuditManager().get(context.audit)
        data = model.objects.get(pk=context.id)

        return actions.PreJsonResult({'data': data})