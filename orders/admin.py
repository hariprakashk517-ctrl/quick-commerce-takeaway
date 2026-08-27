from django.contrib import admin
from .models import * 
# Register your models here.

# admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderStatusHistory)
admin.site.register(ReplacementRequest)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "customer",
        "order_status",
        "fulfillment_mode",
        "payment_status",
        "total_amount",
        "item_count",
        "created_at",
    )

    def item_count(self, obj):
        return obj.items.count()

    item_count.short_description = "Items"



