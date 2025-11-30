from django.contrib import admin
from .models import User , Review , Product ,Payment ,OrderItem , Order , CartItem
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username" ,"email","phone"  , "image_tag"]
    
    def image_tag(self , obj):
        if obj.dp:
            return str(obj.dp)
        
        return "_"
    
    image_tag.description = "Profile Picture"
    
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name" , "image_tag"]
    
    
    def image_tag(self , obj):
        if obj.image:
            return str(obj.image)
        
        return "_"
    
    image_tag.description = "Product Picture"
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["subtotal_display"]

    def subtotal_display(self, obj):
        return f"${obj.subtotal():,.2f}"

    subtotal_display.short_description = "Subtotal"


# --------------------------------------------
# PAYMENT INLINE (one-to-one)
# --------------------------------------------
class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    max_num = 1
    readonly_fields = ["transaction_id", "paid_at"]

@admin.register(Payment)
class payment(admin.ModelAdmin):
    list_display = ["buyer","transaction_id" , "status"]
# --------------------------------------------
# ORDER ADMIN
# --------------------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "buyer", "status", "created_at", "total_display"]
    search_fields = ["id", "buyer__username", "buyer__email"]
    list_filter = ["status", "created_at"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    inlines = [OrderItemInline, PaymentInline]

    readonly_fields = ["total_display", "created_at"]

    fieldsets = (
        ("Order Info", {
            "fields": ("buyer", "status", "created_at", "total_display")
        }),
    )

    def total_display(self, obj):
        return f"${obj.total_price():,.2f}"

    total_display.short_description = "Total Price"


# --------------------------------------------
# REVIEW ADMIN
# --------------------------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "buyer", "rating", "created_at"]
    search_fields = ["product__name", "buyer__username"]
    list_filter = ["rating", "created_at"]
    ordering = ["-created_at"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["product" ,"quantity"]