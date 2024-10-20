# Generated by Django 5.1.1 on 2024-10-17 13:27

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookshelf', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_out_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(default=datetime.datetime(2024, 10, 31, 13, 27, 52, 141948, tzinfo=datetime.timezone.utc))),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('is_returned', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookshelf.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(max_length=50)),
                ('notification_date', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookshelf.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Overdue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overdue_date', models.DateTimeField(auto_now_add=True)),
                ('penalty_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('is_paid', models.BooleanField(default=False)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans.loan')),
            ],
        ),
        migrations.AddIndex(
            model_name='loan',
            index=models.Index(fields=['user'], name='loans_loan_user_id_4ca51c_idx'),
        ),
        migrations.AddIndex(
            model_name='loan',
            index=models.Index(fields=['book'], name='loans_loan_book_id_c5cb65_idx'),
        ),
        migrations.AddIndex(
            model_name='loan',
            index=models.Index(fields=['is_returned'], name='loans_loan_is_retu_c1831b_idx'),
        ),
    ]
