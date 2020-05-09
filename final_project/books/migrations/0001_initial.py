# Generated by Django 2.2.5 on 2020-05-09 20:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('books_view_hide_completed', models.BooleanField(default=False)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('picture', models.ImageField(blank=True, default='defaultProfilePic.jpg', null=True, upload_to='media/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=10000)),
                ('stars', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('recommendation', models.BooleanField(default=True)),
                ('readability', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=50)),
                ('length', models.PositiveIntegerField()),
                ('completed', models.BooleanField(default=False)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.BookGenre')),
                ('reviews', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]