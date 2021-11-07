from django.contrib import admin
from django.contrib.auth.models import User
from .models import Institution

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        user = request.user
        if user not in queryset:
            admins = User.objects.filter(is_staff=True, is_superuser=False)
            admins_to_delete = queryset.filter(is_staff=True, is_superuser=False)
            print(len(admins_to_delete))
            if (len(admins) - len(admins_to_delete)) > 1:
                super(UserAdmin, self).delete_queryset(request, queryset)
            else:
                print("it must be minimum 1 admin")
        else:
            print("user is in queryset")


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'type', 'categories_list']

    def categories_list(self, obj):
        return ", ".join([str(category) for category in obj.categories.all()])


# Register your models here.
