import datetime
from allauth.utils import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages, admin
from django.urls import reverse

from roles.models import Role, RoleChoices, UserProfile

User = get_user_model()

class QuickAdminForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    phone_number = forms.CharField(max_length=20, required=False)

@staff_member_required
def create_admin_user_view(request):
    if request.method == 'POST':
        form = QuickAdminForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                name=form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name']
            )
            user.save()

            # Create profile for admin user

            profile = UserProfile(
                user=user,
                role=Role.objects.get(name=RoleChoices.ADMIN.value),
                country=None,
                phone_number=form.cleaned_data['phone_number'],
                referral_source=None,
                birth_date=datetime.date.today().strftime('%Y-%m-%d'),
                name=form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name'],
            )
            profile.save()

            messages.success(request, f"Admin user '{profile.name}' created successfully!")
            return redirect("/admin/")
    else:
        form = QuickAdminForm()

    context = {
        'form': form,
        'title': 'Quick Create Admin User',
        'site_header': admin.site.site_header,
        'site_title': admin.site.site_title,
    }
    return render(request, 'admin/create_admin_user.html', context)

