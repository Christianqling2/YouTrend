# Generated by Django 4.2 on 2023-04-12 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

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
                (
                    "category_name",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
            ],
            options={
                "db_table": "Category",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Likes",
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
            ],
            options={
                "db_table": "Likes",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="OurUser",
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
                ("password", models.CharField(max_length=128)),
                ("username", models.CharField(max_length=128)),
                ("email", models.CharField(max_length=128)),
            ],
            options={
                "db_table": "User",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Region",
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
                ("region_name", models.CharField(max_length=32)),
            ],
            options={
                "db_table": "Region",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Video",
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
                ("video_title", models.CharField(max_length=128)),
                ("publish_date", models.DateTimeField(blank=True, null=True)),
                ("trending_date", models.DateTimeField(blank=True, null=True)),
                ("tags", models.CharField(blank=True, max_length=512, null=True)),
                ("view_count", models.IntegerField(blank=True, null=True)),
                ("likes_count", models.IntegerField(blank=True, null=True)),
                ("dislikes", models.IntegerField(blank=True, null=True)),
                ("comment_count", models.IntegerField(blank=True, null=True)),
                (
                    "thumbnail_link",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                ("comments_disabled", models.IntegerField(blank=True, null=True)),
                ("ratings_disabled", models.IntegerField(blank=True, null=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=4096, null=True),
                ),
                (
                    "external_video_id",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
            ],
            options={
                "db_table": "Video",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="VideoProposal",
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
                ("title", models.CharField(blank=True, max_length=128, null=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=4096, null=True),
                ),
                ("tags", models.CharField(blank=True, max_length=512, null=True)),
            ],
            options={
                "db_table": "VideoProposal",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="YoutubeChannel",
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
                ("channel_name", models.CharField(max_length=128)),
                (
                    "external_channel_id",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
            ],
            options={
                "db_table": "YouTubeChannel",
                "managed": False,
            },
        ),
    ]
