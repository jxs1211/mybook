from django.db import models


# Create your models here.

# 所有关联信息都在主表上

class book(models.Model):
    name = models.CharField(max_length=20, verbose_name='图书名')
    publish_year = models.DateField(max_length=10, verbose_name='图书出版日期')
    publish_add = models.DateTimeField(verbose_name='图书添加日期', auto_now_add=True)
    price = models.FloatField(verbose_name='图书价格')
    stock = models.IntegerField(verbose_name='图书库存')
    status = models.BooleanField(verbose_name='出版状态:0,未出版 1,已出版', default=True)
    type = models.ForeignKey('type_book', verbose_name='图书类型')
    author = models.ManyToManyField('author', verbose_name='图书作者')
    publisher = models.ForeignKey('publisher', verbose_name='图书出版社')
    info = models.OneToOneField('detail', blank=True, null=True, unique=True, verbose_name='图书详情')  # unique表示为一对一的映射关系

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='图书表'
        verbose_name_plural=verbose_name


class author(models.Model):
    name = models.CharField(max_length=20, verbose_name='作者名称')
    address = models.CharField(max_length=20, verbose_name='作者地址')
    phone = models.CharField(max_length=15, verbose_name='作者联系方式')
    email = models.EmailField(verbose_name='作者邮箱')
    authorinfo = models.TextField(verbose_name='作者简介')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '作者表'
        verbose_name_plural = verbose_name


class type_book(models.Model):
    typebook = models.CharField(max_length=10, verbose_name='图书类型')

    def __str__(self):
        return self.typebook

    class Meta:
        verbose_name = '图书类型表'
        verbose_name_plural = verbose_name


class publisher(models.Model):
    name = models.CharField(max_length=10, verbose_name='出版社名称')
    address = models.CharField(max_length=20, verbose_name='出版社地址')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '出版社表'
        verbose_name_plural = verbose_name


class detail(models.Model):
    chapter = models.CharField(max_length=10, verbose_name='图书章节')
    pages = models.IntegerField(verbose_name='图书页数')
    words = models.IntegerField(verbose_name='图书字数')
    contentinfo = models.TextField(max_length=200, verbose_name='内容简介')
    logo = models.ImageField(verbose_name='图书封面', max_length=100, null=True)
    catalog = models.TextField(verbose_name='图书目录', max_length=200)

    def __str__(self):
        return self.chapter

    class Meta:
        verbose_name = '图书详情表'
        verbose_name_plural = verbose_name



'''

class book(models.Model):
    name = models.CharField(max_length=20, verbose_name='图书名')
    publish_year = models.DateField()
    publish_add = models.DateTimeField()
    price = models.IntegerField()
    stocks = models.IntegerField()
    status = models.BooleanField(verbose_name='')
    type = models.ForeignKey('type_book')
    author = models.ManyToManyField('author')
    publisher = models.ForeignKey('')
    info = models.OneToOneField('details', blank=True, null=True, unique=True)

    def __str__(self):
        return self.name


class type_book(models.Model):
    typebook = models.CharField(max_length=10, verbose_name='图书类型')

    def __str__(self):
        return self.typebook


class author(models.Model):
    name = models.CharField(max_length=20, verbose_name='作者名称')
    address = models.CharField(max_length=20, verbose_name='')
    phone = models.CharField(max_length=11, verbose_name='')
    email = models.CharField(max_length=20,verbose_name='')
    authorinfo = models.TextField(verbose_name='')

    def __str__(self):
        return self.name


class details(models.Model):
    chapter = models.CharField(max_length=10, verbose_name='')
    pages = models.IntegerField(verbose_name='')
    words = models.IntegerField(verbose_name='')
    chapter = models.CharField(max_length=10, verbose_name='')
    chapter = models.CharField(max_length=10, verbose_name='')


class publisher(models.Model):
    name = models.CharField(max_length=10, verbose_name='出版社名称')
    address = models.CharField(max_length=10, verbose_name='出版社地址')
'''
