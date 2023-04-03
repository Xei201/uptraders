from django.contrib import admin

from .models import Menu, TreeMenu


@admin.register(Menu)
class AccrualAdmin(admin.ModelAdmin):
    list_display = ("name_menu", )


@admin.register(TreeMenu)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("name_tree", "menu", "parent")