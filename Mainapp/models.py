from django.db import models
from mongoengine import *

# Create your models here.
from mongoengine import connect
connect('lianjia')      # 连接的数据库名称

class zufang(Document):
    _id = StringField()
    dataDistributionType = IntField(verbose_name='租房类型')
    district = StringField(verbose_name='区县')
    microdistrict = StringField(verbose_name='商圈')
    community = StringField(verbose_name='校区')
    area = IntField(verbose_name='房屋面积')
    orientation = StringField(verbose_name='朝向')
    houseType = StringField(verbose_name='出租类型')
    tags = ListField(verbose_name='标签')
    title = StringField(verbose_name='标题')
    price = IntField(verbose_name='价格')
    city = StringField(verbose_name='城市')
    floor = IntField(verbose_name='楼层')
    distance = IntField(verbose_name='与地铁站距离')
    bathroom_num = IntField(verbose_name='几卫')
    hall_num = IntField(verbose_name='几厅')
    bedroom_num = IntField(verbose_name='几室')
    latitude = StringField(verbose_name='纬度')
    longitude = StringField(verbose_name='经度')
    img = URLField(verbose_name='图片链接')
    detail_url = URLField(verbose_name='详情页')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'zufang'
        verbose_name = '租房信息集合'
