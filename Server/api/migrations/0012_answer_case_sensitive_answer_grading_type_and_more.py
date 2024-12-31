# Generated by Django 5.1.2 on 2024-12-31 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_assignment_created_at_module_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='case_sensitive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='answer',
            name='grading_type',
            field=models.CharField(choices=[('one-word', 'One Word'), ('short-phrase', 'Short Phrase'), ('list', 'List'), ('numerical', 'Numerical')], default='one-word', max_length=20),
        ),
        migrations.AddField(
            model_name='answer',
            name='order_sensitive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='answer',
            name='range',
            field=models.JSONField(blank=True, default=dict, help_text="Range for numerical answers, e.g., {'min': 0, 'max': 100}"),
        ),
        migrations.AddField(
            model_name='answer',
            name='range_sensitive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='markingscheme',
            name='pass_score',
            field=models.PositiveIntegerField(default=0, help_text='Minimum score required to pass'),
        ),
    ]
