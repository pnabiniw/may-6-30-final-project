# Generated by Django 4.2.3 on 2023-07-23 03:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_useraccountactivationkey'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('profile_picture', models.FileField(blank=True, null=True, upload_to='profile_pictures')),
                ('phone_number', models.CharField(max_length=14)),
                ('address', models.CharField(max_length=50)),
                ('about_me', models.TextField(max_length=1000)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
