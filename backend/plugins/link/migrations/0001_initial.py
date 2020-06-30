# Generated by Django 2.2.13 on 2020-06-30 22:07

from django.db import migrations, models
import django.db.models.deletion
import linkit.model_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='link_linkpluginmodel', serialize=False, to='cms.CMSPlugin')),
                ('link', linkit.model_fields.LinkField(allow_label=True, allow_no_follow=True, allow_target=True, name='link', types=['page'])),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
