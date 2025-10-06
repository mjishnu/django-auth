from django.db import migrations, models


def create_categories(apps, _):
    Category = apps.get_model("base", "Category")
    for name in ["Mental Health", "Heart Disease", "Covid19", "Immunization"]:
        Category.objects.get_or_create(name=name)


def delete_categories(apps, _):
    Category = apps.get_model("base", "Category")
    Category.objects.filter(
        name__in=["Mental Health", "Heart Disease", "Covid19", "Immunization"]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.RunPython(create_categories, delete_categories),
    ]
