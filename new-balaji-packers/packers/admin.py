from django.contrib import admin
from .models import Branch, BookingOrder, CustomerReview


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('city', 'badge', 'is_head_office', 'phone', 'order', 'created_at')
    list_editable = ('is_head_office', 'order')
    search_fields = ('city', 'address', 'phone')
    list_filter = ('is_head_office',)
    ordering = ('order', '-is_head_office', 'city')


@admin.register(BookingOrder)
class BookingOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'phone',
        'pickup_city',
        'drop_city',
        'move_date',
        'estimated_price',
        'status',
        'created_at',
    )
    list_filter = ('status', 'pickup_city', 'drop_city', 'created_at')
    search_fields = ('name', 'phone', 'email', 'pickup_city', 'drop_city', 'custom_items', 'notes')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ("Customer Information", {
            'fields': ('name', 'phone', 'email')
        }),
        ("Moving Route & Schedule", {
            'fields': ('pickup_city', 'drop_city', 'move_date')
        }),
        ("Articles & Custom Items", {
            'fields': ('selected_items', 'custom_items', 'estimated_price', 'notes')
        }),
        ("Order Fulfillment Status", {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer_name', 'rating', 'city', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('reviewer_name', 'city', 'review_text')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)
