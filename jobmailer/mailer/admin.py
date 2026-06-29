from django.contrib import admin
from .models import Company, Domain


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("name", "pdf")
    search_fields = ("name",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "contact_name",
        "email",
        "domain",
        "is_active",
        "last_sent",
    )
    search_fields = ("company_name", "email", "contact_name")
    readonly_fields = ("last_sent",)
    actions = ("mark_as_active", "mark_as_inactive")

    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)

    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)

    mark_as_active.short_description = "Mark selected companies as active"
    mark_as_inactive.short_description = "Mark selected companies as inactive"
