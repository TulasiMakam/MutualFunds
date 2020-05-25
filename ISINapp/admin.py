from django.contrib import admin
from ISINapp.models import MutualFunds
# Register your models here.

class MutualFundsAdmin(admin.ModelAdmin):
    list_display = ['ISIN', 'mutual_funds_name']

admin.site.register(MutualFunds)