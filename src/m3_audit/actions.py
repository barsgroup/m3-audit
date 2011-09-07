#coding:utf-8
'''
Created on 06.01.2011

@author: akvarats
'''

from m3.ui import actions

import ui

class BaseAuditUIActions(actions.ActionPack):
    '''
    Базовый пакет действий, который позволяет
    '''
    
    model = None
    acd = []
    
    def __init__(self):
        super(BaseAuditUIActions, self).__init__()
        
        self.rows_action = AuditRowsDataAction()
        self.list_window_action = AuditListWindowAction()
        
        self.actions.extend([self.rows_action,
                             self.list_window_action,])
    
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
    
    def get_rows(self, pre_query, request, context):
        '''
        '''
        return pre_query
    
    def get_list_url(self):
        '''
        Возвращает полный URL до действия на получение окна со списком 
        записей аудита
        '''
        return self.list_window_action.get_absolute_url()
    

class AuditRowsDataAction(actions.Action):
    '''
    Действие на получение списка записей выполненного аудита
    '''
    url = '/rows'
    
    def context_declaration(self):
        '''
        '''
        acd_list = self.parent.get_acd()
        acd_list.extend([actions.ACD(name='start', type=int, required=True, default=-1),
                          actions.ACD(name='limit', type=int, required=True, default=-1),])
        return acd_list
    
    def run(self, request, context):
        '''
        Выполняет построение предварительного запроса и отдает в функцию
        '''
        pre_query = self.parent.model.objects.all()
        query = self.parent.get_rows(pre_query, request, context)
        
        return actions.ExtGridDataQueryResult(data=query,
                                              start=context.start,
                                              limit=context.limit)

class AuditListWindowAction(actions.Action):
    '''
    Получение окна показа списка записей
    '''
    url = '/list-window'
    
    def context_declaration(self):
        return self.parent.get_acd()
    
    def run(self, request, context):
        
        window = ui.AuditListWindow()
        window = self.parent.get_list_window(window, request, context)
        
        if not window.panel_east.items:
            window.panel_east.items.append(ui.DefaultAuditEastPanel())
            
        window.grid_rows.action_data = self.parent.rows_action.__class__
        
        return actions.ExtUIScriptResult(data=window)