# Generated by Django 5.1.2 on 2024-11-05 01:19

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaccion',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='transaccion',
            name='fecha_transaccion',
        ),
        migrations.AddField(
            model_name='transaccion',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('completado', 'Completado')], default='pendiente', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaccion',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='comprador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
