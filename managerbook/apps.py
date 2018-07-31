from django.apps import AppConfig


class ManagerbookConfig(AppConfig):
    name = 'managerbook'


    class Meta:
        verbose_name = '管理图书'
        verbose_name_plural = verbose_name