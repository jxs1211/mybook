import logging
import time

from PIL import Image
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from pure_pagination import Paginator as pure_paginator

from managerbook.form import BookForm, DetailForm
from managerbook.models import book, type_book, detail
# Create your views here.
from mybook.settings import MEDIA_URL

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')


class Edit_Book(View):
    '''
    编辑图书
    '''

    def get(self, request, book_id):
        '''
        回显数据给前端
        :param request:
        :return:
        '''
        print(request.GET)
        print(book_id)
        logging.info(request.GET)
        logging.info(book_id)
        # 获取book_id对应的数据并加载到bookform上，回显到前端
        author_id_list = []
        book_qs = book.objects.filter(id=int(book_id))
        print(book_qs)
        # model_to_dict(book_obj)
        book_dict = model_to_dict(book_qs[0])
        for author in book_dict['author']:
            author_id_list.append(author.id)
        book_dict['author'] = author_id_list
        print(book_dict)
        detail_dict = model_to_dict(detail.objects.get(id=int(book_dict['info'])))
        print(detail_dict)
        book_form = BookForm(initial=book_dict)

        try:
            # 根据book_id获取对应的图书详情并加载到detailform上，回显到前端
            detail_obj = detail.objects.get(id=int(book_dict['info']))
            detail_dict = model_to_dict(detail_obj)
            logging.info(detail_dict)
            detail_form = DetailForm(initial=detail_dict)
        except:
            # 没有detail信息的时候
            detail_obj = None
            detail_form = DetailForm()
        print(detail_obj.logo)
        print(MEDIA_URL + str(detail_obj.logo))
        # print(MEDIA_ROOT+str(detail_obj.logo))
        # print(BASE_DIR+'/'+str(detail_obj.logo))
        return render(request, 'edit_book.html', {
            'book_id': book_id,
            'book_form': book_form,
            'detail_form': detail_form,
            'detail_obj': detail_obj,
        })

    def post(self, request, book_id):
        '''
        获取前端数据
        4种情况：
        有图书详情：需要上传图片
        有图书详情：不需要上传图片
        无图书详情：需要上传图片
        无图书详情：不需要上传图片
        :param request:
        :param book_id:
        :return:
        '''
        print('request.POST')
        print(request.POST)
        logging.info(request.POST)
        print('request.FILES')
        print(request.FILES)
        logging.info(request.FILES)
        book_form = BookForm(request.POST)
        detail_form = DetailForm(request.POST, request.FILES)
        detail_obj = None
        try:
            if book_form.is_valid() and detail_form.is_valid():
                """
                双表单的验证
                """

                # 更新book数据
                book_qs = book.objects.filter(id=int(book_id))
                book_qs.update(
                    name=book_form.cleaned_data['name'],
                    publish_year=book_form.cleaned_data['publish_year'],
                    price=book_form.cleaned_data['price'],
                    stock=book_form.cleaned_data['stock'],
                    status=book_form.cleaned_data['status'],
                    type=book_form.cleaned_data['type'],
                    publisher=book_form.cleaned_data['publisher'],
                )
                book_qs[0].author.set(book_form.cleaned_data['author'])

                print('book更新成功')
                logging.info('book更新成功')
                '''
                判断是否有detail数据，有就更新数据，没有就创建新的detail对象
                '''
                try:
                    detail_qs = detail.objects.filter(id=int(book_id))
                except:
                    detail_qs = None

                if detail_qs:

                    try:
                        '''
                        获取图片文件，并保存
                        '''
                        logo = request.FILES.get('logo')
                        img = Image.open(logo)
                        path = 'media/img/logo/' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + logo.name
                        path = 'media/img/logo/' + logo.name
                        img.save(path)
                        detail_qs.update(
                            chapter=detail_form.cleaned_data['chapter'],
                            pages=detail_form.cleaned_data['pages'],
                            words=detail_form.cleaned_data['words'],
                            contentinfo=detail_form.cleaned_data['contentinfo'],
                            catalog=detail_form.cleaned_data['catalog'],
                            logo=path,  # 保存图片实际是保存路径
                        )
                        print(detail_qs[0].logo)
                        logging.info('detail更新成功，有图片')
                    except:
                        '''
                        保存detail，没有图片'''
                        detail_qs.update(
                            chapter=detail_form.cleaned_data['chapter'],
                            pages=detail_form.cleaned_data['pages'],
                            words=detail_form.cleaned_data['words'],
                            contentinfo=detail_form.cleaned_data['contentinfo'],
                            catalog=detail_form.cleaned_data['catalog'],
                        )
                        logging.info('detail更新成功，没有图片')
                    detail_obj = detail_qs[0]

                else:
                    '''
                    没有详情数据，创建图书详情，并保存到关联的book表字段
                    '''
                    detail_obj = detail()
                    try:
                        # 有提交图片数据
                        detail_obj.chapter = detail_form.cleaned_data['chapter']
                        detail_obj.pages = detail_form.cleaned_data['pages']
                        detail_obj.words = detail_form.cleaned_data['words']
                        detail_obj.contentinfo = detail_form.cleaned_data['contentinfo']
                        detail_obj.catalog = detail_form.cleaned_data['catalog']
                        # 图片保存
                        logo = request.FILES.get('logo')
                        path = 'media/img/logo/' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + logo.name
                        img = Image.open(logo)
                        img.save(path)
                        detail_obj.logo = path
                        detail_obj.save()
                        # 并保存到关联的book表字段
                        book_qs[0].info = detail_obj
                        book_qs[0].save()
                    except:
                        # 没有提交图片数据
                        detail_obj.chapter = detail_form.cleaned_data['chapter']
                        detail_obj.pages = detail_form.cleaned_data['pages']
                        detail_obj.words = detail_form.cleaned_data['words']
                        detail_obj.contentinfo = detail_form.cleaned_data['contentinfo']
                        detail_obj.catalog = detail_form.cleaned_data['catalog']
                        detail_obj.save()
                        # 并保存到关联的book表字段
                        book_qs[0].info = detail_obj
                        book_qs[0].save()
            else:
                pass
        except:
            print(book_form.errors)
            print(detail_form.errors)
            logging.info(book_form.errors)
            logging.info(detail_form.errors)
            pass
        print(detail_obj)
        logging.info(detail_obj)
        return render(request, 'edit_book.html', {
            'book_id': book_id,
            'book_form': book_form,
            'detail_form': detail_form,
            'detail_obj': detail_obj,
        })


class Delete_Book(View):
    '''
    删除图书
    '''

    def post(self, request):
        print(request.POST)
        ret = {'status': '', 'data': ''}
        book_id = request.POST.get('bookid')
        book.objects.filter(id=int(book_id)).delete()
        ret['status'] = 'success'
        return JsonResponse(ret)


class Add_Detail(View):
    '''
    完善书籍详情添加功能
    '''

    def post(self, request):
        print(request.POST)
        print()
        print(request.FILES)
        ret = {'status': '', 'data': ''}
        detail_form = DetailForm(request.POST, request.FILES)
        if detail_form.is_valid():
            detail_obj = detail()
            detail_obj.chapter = detail_form.cleaned_data['chapter']
            detail_obj.pages = detail_form.cleaned_data['pages']
            detail_obj.words = detail_form.cleaned_data['words']
            detail_obj.contentinfo = detail_form.cleaned_data['contentinfo']
            detail_obj.catalog = detail_form.cleaned_data['catalog']

            # 保存图片文件
            logo = detail_form.cleaned_data['logo']
            path = 'media/img/logo/' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + logo.name
            print(logo)
            img = Image.open(logo)
            img.save(path)
            detail_obj.logo = path
            # 保存detail表的数据
            detail_obj.save()

            # 保存主表关联字段info信息
            book_obj = book.objects.get(id=int(request.POST.get('bookid')))
            book_obj.info = detail_obj
            book_obj.save()

            ret['status'] = 'success'
            ret['data'] = '详情添加成功'
            return JsonResponse(ret)
        else:
            ret['data'] = detail_form.errors
            return JsonResponse(ret)


class Add_book(ListView):
    '''
    书籍添加功能
    '''
    template_name = 'add_book.html'
    model = book
    context_object_name = 'book_obj'

    # 获取提交表单数据
    def post(self, request):
        print(request.POST)
        ret = {"status": "", "data": ""}
        book_form = BookForm(request.POST)

        if book_form.is_valid():
            book_obj = book()
            book_obj.name = book_form.cleaned_data['name']
            book_obj.publish_year = book_form.cleaned_data['publish_year']
            book_obj.price = book_form.cleaned_data['price']
            book_obj.stock = book_form.cleaned_data['stocks']
            book_obj.status = book_form.cleaned_data['status']
            book_obj.type_id = book_form.cleaned_data['type']
            book_obj.publisher_id = book_form.cleaned_data['publisher']
            book_obj.save()
            # 由于author字段是多对多关系，所以一定要在save后添加，否则会添加出错
            book_obj.author.add(*book_form.cleaned_data['author'])
            ret['status'] = 'success'
            ret['data'] = '书籍添加成功'
            return JsonResponse(ret)
        else:
            # ret['status'] = 'fail'
            ret['data'] = book_form.errors
            print(ret['data'])
            return JsonResponse(ret)

    def get_context_data(self, **kwargs):
        type_objs = type_book.objects.all()
        search = self.request.GET.get('search', '')  # 搜索选择框
        type = self.request.GET.get('type_option', '')  # 类别选择框(默认全部)的select选项
        status = self.request.GET.get('status', '')

        print('self.request.GET')
        # request.GET的数据结构<QueryDict: {'type_option': ['2'], 'status': ['1'], 'search': ['']}>
        print(self.request.GET)
        try:
            page = self.request.GET.get('page', 1)  # 在MultipleObjectMixin中定义的page_kwarg = 'page'
        except:
            page = 1
        context = super(Add_book, self).get_context_data(**kwargs)
        context['book_obj'] = context['book_obj'].order_by('id')

        # 根据搜索条件查询数据库
        if search and type and status:
            context['book_obj'] = self.model.objects.filter(
                (Q(name__icontains=search) | Q(author__name__icontains=search))
                & Q(type=type) & Q(status=status)).distinct().order_by('id')
        elif status and type:
            print('status and type:')
            context['book_obj'] = self.model.objects.filter(Q(status=status) & Q(type=type)).order_by('id')
        elif type:
            context['book_obj'] = self.model.objects.filter(type=type).order_by('id')
            print('type')
            print(context['book_obj'])
        elif status:
            context['book_obj'] = self.model.objects.filter(status=status).order_by('id')
        elif search:
            print(search)
            context['book_obj'] = self.model.objects.filter(
                Q(name__icontains=search) | Q(author__name__icontains=search)).distinct().order_by('id')
        # else:#默认显示全部数据

        p = Paginator(context['book_obj'], per_page=3)
        p = pure_paginator(context['book_obj'], per_page=1, request=self.request)

        try:
            page_object = p.page(page)
        except:
            page_object = p.page(1)
        context['book_obj'] = page_object
        context['search'] = search
        try:
            # print(type(type))
            context['selected'] = int(type)  # 转换成int才能给前端做比较判断，选中的是哪个id
        except:
            pass
        try:
            print('statis')
            print(status)
            context['status'] = int(status)
        except:
            pass
        context['type_obj'] = type_objs

        # 添加图书时使用的表单
        context['book_form'] = BookForm()
        # 添加图书详情时使用的表单
        context['detail_form'] = DetailForm()

        return context


class index(ListView):
    '''
    首页书籍列表查询功能
    ListView: 这个类是专门处理数据列表展示的。
    Template_name: 定义了html页面
    Model:定义了数据表，ListView的封装可以将表的数据渲染到模板
    Context_object_name：定义了上下文信息（也就是在html中调用的变量名）
    '''
    template_name = 'index.html'  # 复写自TemplateResponseMixin
    model = book  # 复写自TemplateResponseMixin，并且在BaseListView中赋值给self.object_list=self.get_queryset()
    context_object_name = 'book_obj'  # 复写自MultipleObjectMixin并赋值，

    # 然后在BaseListView中通过get调用MultipleObjectMixin的get_context_data方法赋值给context[’book_obj‘]：
    #         if context_object_name is not None:
    #                   context[context_object_name] = queryset
    # context[context_object_name] = queryset# 等同于render里的{'book_obj':book_obj} key值


    # 1 此处已通过复写BaseListView的get方法：（class BaseListView(MultipleObjectMixin, View):）
    # 2 返回前调用MultipleObjectMixin的get_context_data，将相关数据进行赋值，
    # context = self.get_context_data()
    # 3 最后调用TemplateResponseMixin的render_to_response方法将数据渲染到指定模板上
    # return self.render_to_response(context)


    # 继承MutipleObjectMixin对象的get_context_data，调用此方法前，
    # 此时context需要使用的变量template_name、model、context_object_name，都已经在前面赋值


    # def get_queryset(self):


    def get_context_data(self, **kwargs):
        type_objs = type_book.objects.all()
        search = self.request.GET.get('search', '')  # 搜索选择框
        type = self.request.GET.get('type_option', '')  # 类别选择框(默认全部)的select选项
        status = self.request.GET.get('status', '')
        try:
            page = self.request.GET.get('page', 1)  # 在MultipleObjectMixin中定义的page_kwarg = 'page'
            print("request.GET.get('page', 1)")
            print(page)
        except:
            page = 1
        print('(self.request.GET)')
        print(self.request.GET)
        context = super(index, self).get_context_data(**kwargs)
        print('context')
        print(context)  # 此处object_list和book_obj都已有值，就是queryset

        # 如果查询的表字段是或关系，且字段的表关系是多对多关系（如图书表的书名或作者表的作者名存在多多关系），由于笛卡尔积的关系，导致一条数据查询出多条记录（一本书有4个作者，查询出4条记录）
        # 解决办法：1、不要用或关系查询，只选一个字段
        # 解决办法：2、如果必须使用或关系查询，就对查询结果去重
        if status and type and search:
            print('status and type and search:')
            context['book_obj'] = self.model.objects.filter(
                (Q(name__icontains=search) | Q(author__name__icontains=search)) & Q(status=status) & Q(
                    type=type)).distinct().order_by('id')
            # print(context['book_obj'])
        elif status and type:
            print('status and type:')
            context['book_obj'] = self.model.objects.filter(Q(status=status) & Q(type=type)).order_by('id')
        elif type:
            context['book_obj'] = self.model.objects.filter(type=type).order_by('id')
            print('type')
            print(context['book_obj']).order_by('id')
        elif status:
            context['book_obj'] = self.model.objects.filter(status=status).order_by('id')
        elif search:
            print(search)
            context['book_obj'] = self.model.objects.filter(
                Q(name__icontains=search) | Q(author__name__icontains=search)).distinct().order_by('id')

        print(context['book_obj'])
        # p = Paginator(context['book_obj'], request=self.request, per_page=10)
        p = Paginator(context['book_obj'], per_page=3)
        print('p')
        print(p)
        try:
            # 返回请求页码的page object
            people = p.page(page)  # "Returns a Page object for the given 1-based page number."
        except Exception:
            people = p.page(1)

        # print('people')
        # print(people)
        # print('type_obj')
        # print(type_objs)
        # 请求页码的page object，这里只能用book_obj做key值，book_obj是通过前面的context_object_name赋值
        context['book_obj'] = people
        context['type_obj'] = type_objs
        # print('people.has_previous')
        # print(people.has_previous())
        # print('people.has_next')
        # print(people.has_next())
        # print('people.number')
        # print(people.number)  # 3
        # print('people.object_list')
        # print(people.object_list)

        try:
            context['selected'] = int(type)
            print("context['selected']")
            print(context['selected'])
        except:
            context['selected'] = ''
        try:
            context['status'] = int(status)
        except:
            context['status'] = ''
        print(status)
        context['search'] = search
        print('return context')
        print(context)
        return context