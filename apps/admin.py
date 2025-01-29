from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter

from .models import ProductHistory, FinishProductHistory, Category, FinishCategory


@admin.register(ProductHistory)
class ProductHistoryAdmin(admin.ModelAdmin):
    list_display = ('get_nomi', 'soni', 'status_button',)
    list_filter = [

        ("created_at", DateRangeFilter),
        'status',
        'nomi',
        'soni',

    ]

    def has_add_permission(self, request):
        return False

    def get_nomi(self, obj):
        return obj.nomi.nomi

    get_nomi.short_description = 'Nomi'

    def formatted_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')

    formatted_date.short_description = "Sana"

    def status_button(self, obj):
        color = {
            "qabul": "blue",
            "chiqdi": "green",
        }.get(obj.status.lower(), "gray")  # Default rang - gray

        return format_html(
            '<button style="background-color: {}; color: white; border: none; padding: 5px 10px;">{}</button>',
            color,
            obj.status.capitalize(),
        )

    status_button.short_description = "Status"


@admin.register(FinishProductHistory)
class FinishProductHistoryAdmin(admin.ModelAdmin):
    list_display = ('get_nomi', 'soni', 'status_button',)
    list_filter = (
        ('created_at', DateRangeFilter),
        'status',
        'nomi',
        'soni',


    )

    def get_nomi(self, obj):
        return obj.nomi.nomi

    def has_add_permission(self, request):
        return False

    get_nomi.short_description = 'Nomi'

    def formatted_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')

    formatted_date.short_description = "Sana"

    def status_button(self, obj):
        color = {
            "qabul": "blue",
            "chiqdi": "green",
        }.get(obj.status.lower(), "gray")  # Default rang - gray

        return format_html(
            '<button style="background-color: {}; color: white; border: none; padding: 5px 10px;">{}</button>',
            color,
            obj.status.capitalize(),
        )

    status_button.short_description = "Status"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(FinishCategory)
class FinishCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(User)
admin.site.unregister(Group)
