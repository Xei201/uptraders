from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name_menu = models.CharField(primary_key=True,
                                 verbose_name='Menu name',
                                 max_length=255)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name_menu


class TreeMenu(models.Model):
    name_tree = models.CharField(verbose_name='Tree name', max_length=255)

    menu = models.ForeignKey(Menu,
                             verbose_name='Menu name',
                             on_delete=models.CASCADE)

    parent = models.ForeignKey('self',
                               verbose_name='Parent',
                               on_delete=models.CASCADE,
                               default=None,
                               null=True)

    class Meta:
        ordering = ["pk"]

    # Добавить относительный адрес
    def get_absolute_url(self):
        return reverse('menu') + f'?menu={str(self.menu)}&pk={str(self.pk)}'


    def get_menu(self):
        # Возвращает номер меню на основе данных родителя
        pass

    def __str__(self):
        return self.name_tree


