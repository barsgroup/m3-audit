#coding:utf-8
'''
Created on 06.01.2011

@author: akvarats
'''

from django.forms.models import fields_for_model
from django import forms as form_fields

from m3.ui.ext import windows
from m3.ui.ext import panels
from m3.ui.ext import containers
from m3.ui.ext import fields
from m3.ui.ext.misc import store

from manager import AuditManager


class AuditListWindow(windows.ExtWindow):
    '''
    Окно со списком записей аудита
    '''
    def __init__(self, *args, **kwargs):
        super(AuditListWindow, self).__init__(*args, **kwargs)

        self.title = u'Аудит операций'
        self.template_globals = 'm3-audit-list-window.js'

        self.width = 800
        self.height = 550
        self.layout = 'border'
        self.maximizable = True

        self.panel_center = containers.ExtContainer()
        self.panel_center.region = 'center'
        self.panel_center.layout = 'fit'

        self.grid_rows = panels.ExtObjectGrid()
        self.grid_rows.sm = containers.ExtGridRowSelModel(single_select=True)
        self.grid_rows.store.remote_sort = True
        self.grid_rows.handler_click = 'rowClickHandler'

        self.panel_center.items.append(self.grid_rows)
        self.items.extend([self.panel_center,])

    def create_columns(self, columns):
        '''
        Добавляет отображаемые колонки. Реализазация - как в диктах
        '''
        for column in columns:
            if isinstance(column, tuple):
                column_params = { 'data_index': column[0], 'header': column[1],
                                  'sortable': True }
                if len(column)>2:
                    column_params['width'] = column[2]
            elif isinstance(column, dict):
                column_params = column
            else:
                raise Exception('Incorrect parameter column.')
            self.grid_rows.add_column(**column_params)

        
class DefaultEastPanel(panels.ExtPanel):
    '''
    Панель с полями конкретной записи
    '''
    
    def __init__(self, *args, **kwargs):
        super(DefaultEastPanel, self).__init__(*args, **kwargs)

        self.region = 'east'
        self.layout = 'fit'
        self.title = u'Запись аудита'
        self.width = 270
        self.min_width = 200
        self.max_width = 500
        self.split = True
        self.collapsible = True
        self.padding = 5
        self.body_cls = 'x-window-mc'
        self.template_globals = 'm3-audit-list-window.js'

        self.form = containers.ExtForm()
        self.items.append(self.form)
        
        self.init_component(*args, **kwargs)

    def create_fields(self, model, list_fields=[]):
        '''
        Добавляет поля для просмотра записи на основе полей в модели
        '''
        # маппер Django Forms Fields -> ExtFields
        # TODO: использовать общий маппер (если/когда он будет)
        mapper = dict()
        default_field = fields.ExtStringField
        mapper[form_fields.IntegerField] = fields.ExtNumberField
        mapper[form_fields.Textarea] = fields.ExtTextArea
        
        fields_list = fields_for_model(model()).items()
        for key, field in fields_list:
            # если указан list_fields, то исключим поля, ктр в нем нет
            if list_fields and key not in list_fields:
                continue
            
            field_cls = field.widget.__class__
            ext_field = mapper[field_cls]() if field_cls in mapper else default_field()

            ext_field.name = key
            ext_field.label = field.label
            ext_field.read_only = True
            ext_field.anchor = '100%'

            self.form.items.append(ext_field)


class DefaultTopPanel(containers.ExtContainer):
    '''
    Панель с выбором нужного аудита
    '''

    def __init__(self, *args, **kwargs):
        super(DefaultTopPanel, self).__init__(*args, **kwargs)

        self.region = 'north'
        self.layout = 'form'
        self.height = 35
        self.style = {'padding': '5px'}

        self.init_component(*args, **kwargs)
    
    def create_audits_combo(self, current_audit='', list_audits=[]):
        '''
        Создает комбо и формирует спиок аудитов для представления в нем
        '''
        f_audits_combo = fields.ExtComboBox()
        f_audits_combo.name = 'audit_id'
        f_audits_combo.label = u'Аудит'
        f_audits_combo.value = current_audit
        f_audits_combo.value_field = 'id'
        f_audits_combo.display_field = 'name'
        f_audits_combo.trigger_action = 'all'
        f_audits_combo.anchor = '50%'
        f_audits_combo.editable = False
        f_audits_combo.allow_blank = False
        f_audits_combo.handler_select = 'changeAuditHandler'

        # TODO: эту часть можно вынести в базовый экшнпак
        all_audits = AuditManager().list().items()
        row = lambda code, model: (code[0], model.get_verbose_name())
        result = [row(code, model) for code, model in all_audits]
        if list_audits:
            result = [x for x in result if x[0] in list_audits]
        
        f_audits_combo.set_store(store.ExtDataStore(data=result))

        self.items.append(f_audits_combo)