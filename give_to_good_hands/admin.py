from django.contrib import admin
from django.contrib.auth.models import User
from give_to_good_hands.models import Institution

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    user_fields = ['first_name', 'last_name', 'email', 'is_active']
    superuser_fields = ['is_staff', ]

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fields = self.user_fields + self.superuser_fields
        else:
            self.fields = self.user_fields

        return super(UserAdmin, self).get_form(request, obj, **kwargs)

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
    list_display = ('name', 'description', 'type', 'categories_list')

    def categories_list(self, obj):
        return ", ".join([str(category) for category in obj.categories.all()])
