# Generated by Django 4.2.2 on 2023-06-30 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('electric_bill_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='owners',
            name='tempo_bill',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owners', to='electric_bill_app.tempobill'),
        ),
    ]
