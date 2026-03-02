from django.contrib import admin
from roles.models import Role, UserProfile, UserCategory, Demografy, ListDemografyProfile, KeyDates, KeyDatesProfile


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'client_type', 'country', 'status')
    list_filter = ('role', 'client_type', 'status')
    search_fields = ('user__username', 'user__email')


@admin.register(UserCategory)
class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'category', 'status')
    list_filter = ('status',)

@admin.register(Demografy)
class DemografyAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ListDemografyProfile)
class ListDemografyProfileAdmin(admin.ModelAdmin):
    list_display = ('other_name',)

@admin.register(KeyDates)
class KeyDatesAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(KeyDatesProfile)
class KeyDatesProfileAdmin(admin.ModelAdmin):
    list_display = ('other_name',)

