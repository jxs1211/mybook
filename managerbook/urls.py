# !/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import url

from managerbook.views import *

urlpatterns = [
    url(r'^addbook/', Add_book.as_view(), name='add_book'),
    url(r'^add_detail/', Add_Detail.as_view(), name='add_detail'),
    url(r'^delete_book/', Delete_Book.as_view(), name='delete_book'),
    url(r'^edit_book/(?P<book_id>\d+)/$', Edit_Book.as_view(), name='edit_book'),
]
