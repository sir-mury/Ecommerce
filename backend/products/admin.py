from django.contrib import admin
from .models import Product,Tag,Category
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','able_to_sell','category','date_created']
    list_filter = ['able_to_sell', 'date_created']
    search_fields = ['name']
    list_editable = ['price','able_to_sell']
    filter_horizontal = ['tags']
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title','date_created']
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','date_created']