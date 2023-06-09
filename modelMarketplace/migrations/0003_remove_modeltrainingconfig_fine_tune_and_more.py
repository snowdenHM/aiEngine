# Generated by Django 4.1.7 on 2023-06-09 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelMarketplace', '0002_alter_modeltrainingconfig_loss'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modeltrainingconfig',
            name='fine_tune',
        ),
        migrations.RemoveField(
            model_name='modeltrainingconfig',
            name='loss',
        ),
        migrations.RemoveField(
            model_name='modeltrainingconfig',
            name='num_of_layers_unfreeze',
        ),
        migrations.RemoveField(
            model_name='modeltrainingconfig',
            name='number_of_classes',
        ),
        migrations.RemoveField(
            model_name='modeltrainingconfig',
            name='train_data',
        ),
        migrations.RemoveField(
            model_name='modeltrainingconfig',
            name='val_data',
        ),
        migrations.AddField(
            model_name='modeltrainingconfig',
            name='batch_size',
            field=models.PositiveIntegerField(blank=True, choices=[(16, 16), (32, 32), (64, 64), (128, 128)], default=32, null=True),
        ),
        migrations.AddField(
            model_name='modeltrainingconfig',
            name='img_size',
            field=models.PositiveIntegerField(blank=True, choices=[(224, '224x224'), (256, '256x256'), (416, '416x416'), (512, '512x512'), (640, '640x640'), (1024, '1024x1024')], default=640, null=True),
        ),
        migrations.AddField(
            model_name='modeltrainingconfig',
            name='yolo_choice',
            field=models.CharField(blank=True, choices=[('yolov5n', 'YOLOv5 Nano'), ('yolov5s', 'YOLOv5 Small'), ('yolov5m', 'YOLOv5 Medium'), ('yolov5l', 'YOLOv5 Large'), ('yolov5xl', 'YOLOv5 Extra-Large')], default='yolov5s', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='modeltrainingconfig',
            name='optimizer',
            field=models.CharField(blank=True, choices=[('SGD', 'Stochastic Gradient Descent (SGD)'), ('Adam', 'ADAM'), ('AdamW', 'ADAM (Weight Decay)')], default='SGD', max_length=50, null=True),
        ),
    ]
