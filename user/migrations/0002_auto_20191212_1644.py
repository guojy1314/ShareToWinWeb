# Generated by Django 2.0.3 on 2019-12-12 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='college',
            field=models.CharField(blank=True, choices=[('OT', '其他'), ('CG', '城市经济与公共管理学院'), ('GS', '工商管理学院'), ('JJ', '经济学院'), ('KJ', '会计学院'), ('LJ', '劳动经济学院'), ('WC', '文化与传播学院'), ('GG', '管理工程学院'), ('CS', '财政税务学院'), ('F', '法学院'), ('JR', '金融学院'), ('TJ', '统计学院'), ('WGY', '外国语学院'), ('HQ', '华侨学院'), ('MKS', '马克思主义学院'), ('GJG', '国际经济管理学院'), ('CJ', '国际学院'), ('JX', '继续教育学院')], default='OT', max_length=100, null=True, verbose_name='学院'),
        ),
    ]