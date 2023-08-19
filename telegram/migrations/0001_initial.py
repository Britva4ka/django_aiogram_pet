# Generated by Django 4.2.4 on 2023-08-02 14:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.IntegerField(unique=True)),
                ('username', models.CharField(max_length=64)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('is_admin', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Telegram Пользователь',
                'verbose_name_plural': 'Telegram Пользователи',
                'db_table': 'telegram_user',
                'ordering': ['username'],
            },
        ),
        migrations.CreateModel(
            name='WeatherSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timezone', models.CharField(max_length=64)),
                ('format', models.CharField(choices=[('txt', 'Текстовое уведомление'), ('csv', 'Табличка CSV')], default='txt', max_length=5)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('telegram_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weather_sub', to='telegram.telegramuser')),
            ],
            options={
                'verbose_name': 'Подписка на погоду',
                'verbose_name_plural': 'Подписки на погоду',
                'db_table': 'telegram_weather_subscription',
                'ordering': ['telegram_user'],
            },
        ),
    ]