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
