# Generated by Django 2.0.5 on 2018-06-10 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bias', models.BooleanField(default=False)),
                ('momento', models.BooleanField(default=False)),
                ('funcao_transferencia', models.CharField(choices=[('SG', 'Sigmóide'), ('TH', 'Tangente Hiperbólica')], max_length=1)),
                ('intervalo', models.CharField(choices=[('1', '[0, 1]'), ('2', '[-1, 0]'), ('3', '[-1, 1]'), ('4', '[-0.1, 0.1]')], max_length=1)),
            ],
        ),
    ]
