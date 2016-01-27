# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DefaultModelChangeAuditModel'
        db.create_table('m3_audit_model_changes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(default=u'', max_length=50, null=True, db_index=True, blank=True)),
            ('userid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('user_fio', self.gf('django.db.models.fields.CharField')(default=u'', max_length=70, null=True, db_index=True, blank=True)),
            ('user_info', self.gf('django.db.models.fields.CharField')(default=u'', max_length=200, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('object_model', self.gf('django.db.models.fields.CharField')(max_length=300, db_index=True)),
            ('object_data', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('m3_audit', ['DefaultModelChangeAuditModel'])

        # Adding model 'DictChangesAuditModel'
        db.create_table('m3_audit_dict_changes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(default=u'', max_length=50, null=True, db_index=True, blank=True)),
            ('userid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('user_fio', self.gf('django.db.models.fields.CharField')(default=u'', max_length=70, null=True, db_index=True, blank=True)),
            ('user_info', self.gf('django.db.models.fields.CharField')(default=u'', max_length=200, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('object_model', self.gf('django.db.models.fields.CharField')(max_length=300, db_index=True)),
            ('object_data', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('m3_audit', ['DictChangesAuditModel'])

        # Adding model 'AuthAuditModel'
        db.create_table('m3_audit_auth', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(default=u'', max_length=50, null=True, db_index=True, blank=True)),
            ('userid', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('user_fio', self.gf('django.db.models.fields.CharField')(default=u'', max_length=70, null=True, db_index=True, blank=True)),
            ('user_info', self.gf('django.db.models.fields.CharField')(default=u'', max_length=200, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('m3_audit', ['AuthAuditModel'])


    def backwards(self, orm):
        
        # Deleting model 'DefaultModelChangeAuditModel'
        db.delete_table('m3_audit_model_changes')

        # Deleting model 'DictChangesAuditModel'
        db.delete_table('m3_audit_dict_changes')

        # Deleting model 'AuthAuditModel'
        db.delete_table('m3_audit_auth')


    models = {
        'm3_audit.authauditmodel': {
            'Meta': {'object_name': 'AuthAuditModel', 'db_table': "'m3_audit_auth'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'user_fio': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '70', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'user_info': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'userid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '50', 'null': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        'm3_audit.defaultmodelchangeauditmodel': {
            'Meta': {'object_name': 'DefaultModelChangeAuditModel', 'db_table': "'m3_audit_model_changes'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_data': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'object_model': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_index': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'user_fio': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '70', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'user_info': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'userid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '50', 'null': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        'm3_audit.dictchangesauditmodel': {
            'Meta': {'object_name': 'DictChangesAuditModel', 'db_table': "'m3_audit_dict_changes'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_data': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'object_model': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_index': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'user_fio': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '70', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'user_info': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'userid': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '50', 'null': 'True', 'db_index': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['m3_audit']
