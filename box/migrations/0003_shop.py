# Generated by Django 3.2.4 on 2021-08-16 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('box', '0002_alter_diaclase_lista_estudiante'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensualidad', models.CharField(max_length=100)),
                ('items', models.CharField(max_length=100, null=True)),
                ('pagado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='box.user')),
            ],
        ),
    ]
