var grid_rows = Ext.getCmp('{{ component.grid_rows.client_id }}');
var form_details = Ext.getCmp('{{ component.form_details.client_id }}');
var url_audit_win = '{{ component.url_audit_win }}';
var url_audit_row = '{{ component.url_audit_row }}';

function rowChangeHandler(e){
    win.fireEvent('auditRowClick', grid_rows);

    if (form_details && url_audit_row) {
		var selModel = grid_rows.getSelectionModel();
        if (selModel.hasSelection()) {
			Ext.Ajax.request({
				url: url_audit_row
				,method: 'POST'
				,params: {
					id: selModel.getSelected().id,
					audit: win.actionContextJson.audit
				}
				,success: function(response, opts){
					var json = Ext.util.JSON.decode(response.responseText);
					form_details.getForm().setValues(json.data);
				}
				,failure: function(response, opts){
					uiAjaxFailMessage.apply(this, arguments);
				}
			});
        }
    }
}

function changeAuditHandler(cml, record, recId){
    // при смене аудита в комбо, закрывает текущее окно и
    // открывает такое же, но с другим аудитом
    assert(url_audit_win, 'Не задан url окна со списком аудита!');

	var audit = record.get('id');
	Ext.Ajax.request({
		url: url_audit_win
		,method: 'POST'
		,params: { audit: audit }
		,success: function(response, opts){
			var newWin = smart_eval(response.responseText);
			newWin.show();
			win.close();
		}
		,failure: function(response, opts){
			uiAjaxFailMessage.apply(this, arguments);
		}
	});
}


{% block extenders %}
{# место, куда вставлять код из дочернего прикладного окошка #}
{% endblock %}