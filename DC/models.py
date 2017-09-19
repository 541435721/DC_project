# coding:utf-8
from django.db import models


# Create your models here.

class Students(models.Model):  # 学生表
    user_id = models.CharField(max_length=30, primary_key=True)  # 学号

    def __str__(self):
        return str(self.user_id)


class Borrow_records(models.Model):  # 借阅记录
    # user_id = models.ForeignKey(Students, on_delete=models.CASCADE)  # 学号
    user_id = models.CharField(max_length=30)  # 学号
    book_id = models.CharField(max_length=50)  # 图书号
    time = models.DateField()  # 借阅时间

    def __str__(self):
        return str(self.user_id)


class Schoolarship(models.Model):  # 奖学金
    # user_id = models.ForeignKey(Students, on_delete=models.CASCADE)  # 学号
    user_id = models.CharField(max_length=30)  # 学号
    level = models.IntegerField()  # 奖学金等级

    def __str__(self):
        return str(self.user_id)


class Scores(models.Model):  # 学生成绩
    # user_id = models.ForeignKey(Students, on_delete=models.CASCADE)  # 学号
    user_id = models.CharField(max_length=30)  # 学号
    year = models.CharField(max_length=20)  # 学年
    semester = models.CharField(max_length=20)  # 学期
    course_id = models.CharField(max_length=50)  # 课程号
    score = models.IntegerField()  # 分数

    def __str__(self):
        return str(self.user_id)


class Job(models.Model):  # 就业信息
    # user_id = models.ForeignKey(Students, on_delete=models.CASCADE)  # 学号
    user_id = models.CharField(max_length=30)  # 学号
    address = models.CharField(max_length=30, null=True)  # 工作地点
    salary = models.IntegerField(null=True)  # 薪水

    def __str__(self):
        return str(self.user_id)


class Cost(models.Model):
    # user_id = models.ForeignKey(Students, on_delete=models.CASCADE)  # 学号
    user_id = models.CharField(max_length=30)  # 学号
    consume_type = models.CharField(max_length=10, null=True)  # 消费类型
    consume_address = models.CharField(max_length=50, null=True)  # 消费地点
    shopping_time = models.DateTimeField()  # 消费时间
    price = models.FloatField()  # 消费价格

    def __str__(self):
        return str(self.user_id)


class Messages(models.Model):
    # user_id = models.ForeignKey(Students, on_delete=models.CASCADE)  # 学号# 学号
    user_id = models.CharField(max_length=30)  # 学号
    time = models.DateField()  # 发帖时间
    mount = models.IntegerField()  # 发帖数目

    def __str__(self):
        return str(self.user_id)


class House(models.Model):
    name = models.CharField(max_length=100)  # 楼盘名称
    type = models.CharField(max_length=30)  # 楼盘类型
    price = models.CharField(max_length=30)  # 均价
    features = models.CharField(max_length=100)  # 楼盘特征
    city = models.CharField(max_length=30)  # 楼盘位置
    address = models.CharField(max_length=200)  # 楼盘地址
    sale_address = models.CharField(max_length=200)  # 售楼地址
    developer = models.CharField(max_length=100)  # 开发商
    building_type = models.CharField(max_length=100)  # 建筑类型
    green_ratio = models.CharField(max_length=30)  # 绿化率
    square = models.CharField(max_length=30)  # 占地面积
    Volume_ratio = models.CharField(max_length=30)  # 容积率
    building_square = models.CharField(max_length=30)  # 见你住面积
    owner = models.CharField(max_length=30)  # 规划用户
    property_right_years = models.CharField(max_length=30)  # 产权
    estate_type = models.CharField(max_length=20)  # 楼盘户型
    property_company = models.CharField(max_length=200)  # 物业公司
    parking_space_ratio = models.CharField(max_length=30)  # 车位配比
    property_fee = models.CharField(max_length=30)  # 物业费
    heating_mode = models.CharField(max_length=30)  # 供暖方式
    water_supply_mode = models.CharField(max_length=30)  # 供水方式
    power_supply_mode = models.CharField(max_length=30)  # 供电方式

    def __str__(self):
        return str(self.name)
