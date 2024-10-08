# Generated by Django 5.1 on 2024-09-13 02:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abnt_model', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Simple_TCC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_do_arquivo', models.TextField()),
                ('autor', models.TextField()),
                ('titulo', models.TextField()),
                ('introducao', models.TextField()),
                ('desenvolvimento', models.TextField()),
                ('conclusao', models.TextField()),
                ('url_imagem', models.URLField(blank=True, null=True)),
                ('instituicao', models.TextField()),
                ('ano', models.TextField()),
                ('resumo', models.TextField()),
                ('palavras_chaves', models.TextField()),
                ('abstract', models.TextField()),
                ('keyword', models.TextField()),
                ('problematização', models.TextField()),
                ('justificativa', models.TextField()),
                ('questao_geral', models.TextField()),
                ('objetivo', models.TextField()),
                ('metodologia', models.TextField()),
                ('analise_discussao', models.TextField()),
                ('referencias', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
