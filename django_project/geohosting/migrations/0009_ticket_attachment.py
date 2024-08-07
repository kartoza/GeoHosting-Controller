# Generated by Django 4.2.7 on 2024-08-08 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geohosting', '0008_userprofile_reset_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('pending', 'Pending')], default='open', max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='ticket_attachments/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='geohosting.ticket')),
            ],
        ),
    ]
