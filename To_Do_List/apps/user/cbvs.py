from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from apps.user.forms import SignupForm, LoginForm
from utils.email import send_email



User = get_user_model()

class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("cbv_user:login")

    def form_valid(self, form):
        user = form.save()
        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)

        url = f'{self.request.scheme}://{self.request.META["HTTP_HOST"]}/cbv/verify/?code={signer_dump}'

        if settings.DEBUG:
            print(url)
        else:
            subject = '[Todo] 이메일 인증'
            message = f'다음 링크를 클릭해주세요. {url}'

            send_email(subject=subject, message=message, to_email=user.email)

        return render(
            request=self.request,
            template_name="registration/signup_done.html",
            context={
                'user': user,
            }
        )

def verify_email(request):
    code = request.GET.get('code', '')

    signer = TimestampSigner()
    try:
        decoded_user_email = signing.loads(code)
        user_email = signer.unsign(decoded_user_email, max_age=60*10)
    except (TypeError, SignatureExpired):
        return render(request, 'registration/verify_failed.html')

    user = get_object_or_404(User, email=user_email)
    user.is_active = True
    user.save()
    return render(request, 'registration/verify_success.html')


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("cbv_todo:list")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        next_page = self.request.GET.get('next')
        if next_page:
            return HttpResponseRedirect(next_page)

        return HttpResponseRedirect(self.get_success_url())

