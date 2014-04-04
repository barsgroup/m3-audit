#coding:utf-8
u"""
.. Created on 07.01.2011

.. @author: akvarats
"""


#===============================================================================
# js shortcuts
#===============================================================================

def js_audit_list_window(audit_pack, parent_window):
    u"""
    Возвращает js код, который может быть использован для показа окна
    с результатами аудита

    :param audit_pack: пак аудита
    :type audit_pack: :py:class:`m3_audit.actions.BaseAuditUIActions`
    :param parent_window: родительское окно
    :type parent_window: :py:class:`m3.ui.ext.windows.ExtWindow`
    """
    js_template = '''function (){{
    var parent_window = Ext.getCmp('{parent_window_client_id}');
    var params = {{}};
    Ext.applyIf(params, parent_window.actionContextJson);
    var loadMask = new Ext.LoadMask(win.body);
    loadMask.show();
    Ext.Ajax.request({{
        method: 'POST',
        url: '{action_url}',
        params: params,
        success: function(response, opts){{
           loadMask.hide();
           smart_eval(response.responseText); 
        }},
        failure: function (response, opts){{
            loadMask.hide();
            uiAjaxFailMessage.apply(this, arguments);
        }}
    }});
}}'''

    return js_template.format(parent_window_client_id=parent_window.client_id,
                              action_url=audit_pack.get_list_url())