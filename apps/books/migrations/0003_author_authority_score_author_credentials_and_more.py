# Generated manually for author authority fields

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0002_book_electronic_price_book_price_book_url_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="authority_score",
            field=models.IntegerField(
                blank=True,
                help_text="Автоматически рассчитывается на основе регалий",
                null=True,
                verbose_name="Оценка авторитетности (0-100)",
            ),
        ),
        migrations.AddField(
            model_name="author",
            name="credentials",
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text="JSON с данными о публикациях, наградах, должностях",
                verbose_name="Регалии и достижения",
            ),
        ),
        migrations.AddField(
            model_name="author",
            name="credentials_updated_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Дата обновления регалий"
            ),
        ),
        migrations.AlterModelOptions(
            name="author",
            options={
                "ordering": ["-authority_score", "last_name", "first_name"],
                "verbose_name": "Автор",
                "verbose_name_plural": "Авторы",
            },
        ),
    ]
