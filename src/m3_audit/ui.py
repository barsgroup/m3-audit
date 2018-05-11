#coding:utf-8
u"""
Окна информации аудитов
-----------------------

.. Created on 06.01.2011

.. @author: akvarats
"""
# TODO: можно же импортнуть в одну строчку все
from __future__ import absolute_import
from m3.ui.ext import windows
from m3.ui.ext import panels
from m3.ui.ext import containers
from m3.ui.ext import fields
from m3.ui.ext.misc import store

# TODO: не используется в модуле
from .helpers import ext_fields_for_model


class AuditListWindow(windows.ExtWindow):
    u"""
    Окно со списком записей аудита
    """
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
        self.grid_rows.handler_click = 'rowChangeHandler'
        # TODO: может хватит и append
        self.grid_rows.plugins.extend([
            'new Ext.ux.grid.GridHeaderFilters()',
        ])
        
        self.panel_center.items.append(self.grid_rows)
        # TODO: может хватит и append
        self.items.extend([self.panel_center,])

    def create_columns(self, columns, model=None):
        u"""
        Добавляет в грид колокни

        :param columns: добавляемые колонки
        :type columns: list, tuple
        :param model: модель аудита
        :type model: :py:class:`django.db.models.Models`
        """

        # получим поля модели в виде ExtFields,
        # чтобы сформировать подходящие хэдэр-фильтры
        model_ext_fields = ext_fields_for_model(model)

        for column in columns:
            if isinstance(column, tuple):
                column_params = {'data_index': column[0], 'header': column[1],
                                 'sortable': True}
                if len(column) > 2:
                    column_params['width'] = column[2]
            elif isinstance(column, dict):
                column_params = column
            else:
                raise Exception('Incorrect parameter column.')

            if column[0] in model_ext_fields:
                ext_field = model_ext_fields[column[0]]
                column_params['extra'] = {
                    'filter': ext_field.render(),
                }
                # для enum-колонок сформируем рендерер, ктр будет заменять id
                # на человеческие значения
                if hasattr(ext_field, 'store'):
                    renderer = u'function(v){var store={%s};return store[v]}' %\
                               ','.join('"%s":"%s"' % (key, val) for key, val in ext_field.store.data)
                    column_params['extra']['renderer'] = renderer

            self.grid_rows.add_column(**column_params)


class DefaultEastPanel(panels.ExtPanel):
    u"""
    Панель с полями конкретной записи
    """
    
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

    def create_fields(self, model):
        u"""
        Добавляет поля из модели, для просмотра записи на основе полей в модели

        :param model: модель аудита
        :type model: :py:class:`django.db.models.Models`
        """
        ext_fields = ext_fields_for_model(model)

        if model.list_fields:
            # если указаны кастомные поля для отображения, то добавляем на форму их
            list_fields = model.list_fields
        else:
            # в противном случае - все поля модели
            list_fields = list(ext_fields.keys())

        for field_name in list_fields:
            if field_name in ext_fields:
                ext_field = ext_fields[field_name]
                ext_field.read_only = True
                ext_field.anchor = '100%'

                self.form.items.append(ext_field)


class DefaultTopPanel(containers.ExtContainer):
    u"""
    Панель с выбором нужного аудита
    """

    def __init__(self, *args, **kwargs):
        super(DefaultTopPanel, self).__init__(*args, **kwargs)

        self.region = 'north'
        self.layout = 'form'
        self.height = 35
        self.style = {'padding': '5px'}

        self.init_component(*args, **kwargs)
    
    def create_audits_combo(self, list_audits, current_audit=''):
        u"""
        Создает комбо со списком аудитов для перехода между ними

        :param list_audits: список аудитов
        :type list_audits: list
        :param current_audit: теукщий аудит
        :type current_audit: str
        """
        # TODO: почему бы не определять параметры объекта при его инициализации
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
        f_audits_combo.set_store(store.ExtDataStore(data=list_audits))

        self.items.append(f_audits_combo)