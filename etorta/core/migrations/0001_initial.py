# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Loja'
        db.create_table(u'core_loja', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Loja'])

        # Adding model 'Cliente'
        db.create_table(u'core_cliente', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('loja', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Loja'])),
        ))
        db.send_create_signal(u'core', ['Cliente'])

        # Adding model 'Produto'
        db.create_table(u'core_produto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('disponibilidade', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('codigo', self.gf('django.db.models.fields.IntegerField')()),
            ('preco', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'core', ['Produto'])

        # Adding model 'Url'
        db.create_table(u'core_url', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('endereco', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('disponibilidade', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('loja', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Loja'])),
            ('produto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Produto'])),
        ))
        db.send_create_signal(u'core', ['Url'])


    def backwards(self, orm):
        # Deleting model 'Loja'
        db.delete_table(u'core_loja')

        # Deleting model 'Cliente'
        db.delete_table(u'core_cliente')

        # Deleting model 'Produto'
        db.delete_table(u'core_produto')

        # Deleting model 'Url'
        db.delete_table(u'core_url')


    models = {
        u'core.cliente': {
            'Meta': {'object_name': 'Cliente'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loja': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Loja']"}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.loja': {
            'Meta': {'object_name': 'Loja'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'produtos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Produto']", 'through': u"orm['core.Url']", 'symmetrical': 'False'})
        },
        u'core.produto': {
            'Meta': {'object_name': 'Produto'},
            'codigo': ('django.db.models.fields.IntegerField', [], {}),
            'disponibilidade': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'preco': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'core.url': {
            'Meta': {'object_name': 'Url'},
            'disponibilidade': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loja': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Loja']"}),
            'produto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Produto']"})
        }
    }

    complete_apps = ['core']