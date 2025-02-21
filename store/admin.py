from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'digital')
    list_filter = ('category', 'digital')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'customer', 'date_ordered', 'complete', 'status')
    list_filter = ('complete', 'status', 'date_ordered')
    search_fields = ('transaction_id', 'customer__name')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity')
    list_filter = ('order__complete',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(ShippingAddress)