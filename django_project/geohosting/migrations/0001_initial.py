# Generated by Django 4.2.7 on 2024-07-08 15:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import geohosting.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ActivityType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "identifier",
                    models.CharField(
                        help_text="Activity type.", max_length=256, unique=True
                    ),
                ),
                (
                    "jenkins_url",
                    models.CharField(
                        help_text="Jenkins URL based on identifier and product (optional).",
                        max_length=256,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Cluster",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=256)),
                ("url", models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("upstream_id", models.CharField(max_length=256)),
                ("description", models.TextField(blank=True)),
                (
                    "image",
                    geohosting.models.fields.SVGAndImageField(
                        blank=True, null=True, upload_to="product_images/"
                    ),
                ),
                ("available", models.BooleanField(default=False)),
                (
                    "cluster",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="geohosting.cluster",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("code", models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProductMedia",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="product_media/")),
                ("description", models.TextField(blank=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="geohosting.product",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cluster",
            name="region",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="geohosting.region"
            ),
        ),
        migrations.CreateModel(
            name="Activity",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "client_data",
                    models.JSONField(
                        blank=True, help_text="Data received from client.", null=True
                    ),
                ),
                ("post_data", models.JSONField(blank=True, null=True)),
                (
                    "triggered_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("RUNNING", "RUNNING"),
                            ("BUILD_JENKINS", "BUILD_JENKINS"),
                            ("BUILD_ARGO", "BUILD_ARGO"),
                            ("ERROR", "ERROR"),
                            ("SUCCESS", "SUCCESS"),
                        ],
                        default="RUNNING",
                        help_text="The status of activity.",
                        max_length=256,
                    ),
                ),
                (
                    "note",
                    models.TextField(
                        blank=True, help_text="Note about activity.", null=True
                    ),
                ),
                (
                    "jenkins_queue_url",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "jenkins_build_url",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "activity_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="geohosting.activitytype",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="geohosting.product",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Activities",
                "ordering": ("-triggered_at",),
            },
        ),
        migrations.CreateModel(
            name="Instance",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("package_id", models.CharField(max_length=256)),
                ("owner_email", models.CharField(max_length=256)),
                (
                    "cluster",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="geohosting.cluster",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="geohosting.product",
                    ),
                ),
            ],
            options={
                "unique_together": {("name", "cluster")},
            },
        ),
        migrations.AlterUniqueTogether(
            name="cluster",
            unique_together={("code", "region")},
        ),
    ]
