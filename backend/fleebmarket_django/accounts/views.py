from django.shortcuts import render
from django.views.generic import View
from django.conf import settings
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.base import ContextMixin
from django.template.response import TemplateResponse
from .models import CustomUser
from allauth.socialaccount.models import SocialAccount

class Profile(View):

    def get(self, request):
        user = request.user
        social_accounts = SocialAccount.objects.filter(
            user=user
        )
        context = {
            'user': user,
            'social_accounts': social_accounts
        }

        return render(request, 'accounts/profile.html', context)


class ProfileUpdate(UpdateView):
    model = CustomUser
    fields = ("country", )
    success_url = ''

    # Check we can only edit current user
    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        if self.request.user == self.object:
            return res
        return None
