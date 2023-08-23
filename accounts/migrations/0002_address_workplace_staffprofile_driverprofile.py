# Generated by Django 4.1.6 on 2023-08-22 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('house_number', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StaffProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=300, null=True, unique=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('father_name', models.CharField(max_length=200)),
                ('gender', models.CharField(choices=[('آقا', 'آقا'), ('خانم', 'خانم')], default='آقا', max_length=5)),
                ('tazkira_num', models.CharField(max_length=255)),
                ('phone_num', models.CharField(blank=True, max_length=14, null=True, unique=True)),
                ('tazkira_img', models.ImageField(upload_to='media/staff/id_images')),
                ('avatar', models.ImageField(blank=True, default='media/staff.jpg', null=True, upload_to='media/staff/profile_images')),
                ('current_address', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.address')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('work_place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.workplace')),
            ],
        ),
        migrations.CreateModel(
            name='DriverProfile',
            fields=[
                ('licence_num', models.CharField(max_length=250, unique=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('father_name', models.CharField(max_length=200)),
                ('gender', models.CharField(choices=[('آقا', 'آقا'), ('خانم', 'خانم')], default='آقا', max_length=5)),
                ('blood_group', models.CharField(blank=True, max_length=10, null=True)),
                ('tazkira_num', models.CharField(max_length=255)),
                ('phone_num', models.CharField(blank=True, max_length=14, null=True, unique=True)),
                ('tazkira_img', models.ImageField(blank=True, default='media/driver_id.jpg', null=True, upload_to='media/driver/id_images')),
                ('avatar', models.ImageField(blank=True, default='media/driver.jpg', null=True, upload_to='media/driver/profile_images')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('current_address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.address')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
