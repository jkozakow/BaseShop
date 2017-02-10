from django.contrib import admin
from baseshop import models
from authentication.models import CustomUser

admin.site.register(CustomUser)
admin.site.register(models.TV)
admin.site.register(models.Laptop)
admin.site.register(models.Phone)
admin.site.register(models.Processor)
admin.site.register(models.GraphicCard)
admin.site.register(models.BaseProduct)

admin.site.register(models.TVManufacturer)
admin.site.register(models.LaptopManufacturer)
admin.site.register(models.PhoneManufacturer)
admin.site.register(models.ProcessorManufacturer)


class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    readonly_fields = ('product', 'quantity', 'total_price')
    can_delete = False

    def has_add_permission(self, request):
        return False


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]
    readonly_fields = ('user', 'shipping_address', 'total_price')
    list_display = ('__str__', 'completed',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(models.Order, OrderAdmin)
