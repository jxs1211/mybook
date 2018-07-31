from django.contrib import admin

from .models import *

# Register your models here.


class bookAdmin(admin.ModelAdmin):
    list_display = ('id','name','publish_year','price','stock','type') #添加字段显示
    list_display_links = ('name','publish_year',)
    search_fields = ('name',) #添加快速查询栏



admin.site.register(book,bookAdmin)
admin.site.register(author)
admin.site.register(publisher)
admin.site.register(type_book)
admin.site.register(detail)
