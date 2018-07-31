# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets

from .models import author, type_book, publisher


class BookForm(forms.Form):
    name = forms.CharField(
        max_length=20,
        min_length=2,
        widget=widgets.TextInput(  # 选择html控件
            attrs={
                'class': 'form-control',  # 设置控件属性，如设置class的样式
                'placeholder': '书名',
                'id': 'bookname',
            }
        )
    )

    publish_year = forms.DateField(
        widget=widgets.DateInput(
            attrs={
                'placeholder': '出版日期：2017-01-01',
                'class': 'form-control',
                'id': 'publish_year',
            }
        ),
    )

    price = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={
                'placeholder': '价格',
                'class': 'form-control',
                'id': 'price',
            }
        )
    )
    stock = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={
                'placeholder': '库存',
                'class': 'form-control',
                'id': 'stocks',
            }
        )
    )
    author = forms.MultipleChoiceField(
        choices=author.objects.all().values_list('id', 'name'),  # 将queryset转换成list
        widget=widgets.SelectMultiple(
            attrs={
                'id': 'demo-cs-multiselect',
                # 'value': '作者选择',
            }
        )
    )
    status = forms.ChoiceField(
        choices=[(1, '出版'), (2, '未出版'), ],
        widget=widgets.Select(
            attrs={
                'type': 'select',
                'class': 'magic-select',
                'id': 'status',
            }
        )
    )

    type = forms.ChoiceField(
        choices=type_book.objects.all().values_list('id', 'typebook'),
        widget=widgets.Select(
            attrs={
                "data-live-search": "true",
                "data-width": "100%",
                'class': 'selectpicker',
                'id': 'type',
            }
        )
    )
    publisher = forms.ChoiceField(
        choices=publisher.objects.all().values_list('id', 'name'),
        widget=widgets.Select(
            attrs={
                'class': 'selectpicker',
                'data-live-search': 'True',
                'data-width': '100%',
                'id': 'publisher',
            }
        )
    )


class DetailForm(forms.Form):
    chapter = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={
                'placeholder': '章节',
                'class': 'form-control',
                'id': 'chapter',
            }
        )
    )

    pages = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={
                'placeholder': '页数',
                'class': 'form-control',
                'id': 'pages',
            }
        )
    )

    words = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={
                'placeholder': '字数',
                'class': 'form-control',
                'id': 'words',
            }
        )
    )

    contentinfo = forms.CharField(
        widget=widgets.Textarea(
            attrs={
                'rows': 8,
                'placeholder': '图书简介',
                'class': 'form-control',
                'id': 'demo-textarea-input-1',
            }
        )
    )
    catalog = forms.CharField(
        widget=widgets.Textarea(
            attrs={
                'rows': 8,
                'placeholder': '目录',
                'class': 'form-control',
                'id': 'demo-textarea-input-2',
            }
        )
    )
    logo = forms.ImageField(
        allow_empty_file=True,
        widget=widgets.FileInput(
            attrs={
                'id': 'logo_file',
                'class': 'file-input-new btn btn-primary btn-file',
                'style': " margin: auto;",
                'required':'false',
            }
        )
    )
