from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.user.forms import SignupForm


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("login")


