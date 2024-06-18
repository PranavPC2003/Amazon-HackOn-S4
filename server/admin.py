from django.contrib import admin
from django.db import IntegrityError
from .models import UserProfile, Category, Items, Bank_Info, Orders, Set_Budget

# class SetBudgetAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         try:
#             obj.save()
#         except IntegrityError:
#             existing_obj = Set_Budget.objects.get(user=obj.user, date__month=obj.date.month)
#             existing_obj.amount = obj.amount
#             existing_obj.save()

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Items)
admin.site.register(Bank_Info)
admin.site.register(Orders)
admin.site.register(Set_Budget)
