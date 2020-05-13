from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from . import forms

class SignupView(CreateView):
    form_class=forms.SignupForm
    template_name='account/signup.html'
    success_url=reverse_lazy('login')
    verify_url=reverse_lazy('verify')
    email_template_name='account/registration_verification.html'
    token_generator=default_token_generator

    def form_valid(self, form):
        response=super().form_valid(form)
        if form.instance:
            self.send_verification_email(form.instance)
        return response

    def send_verification_email(self, user):
        token=self.token_generator.make_token(user)
        url=self.build_verification_link(user, token)
        subject='회원가입을 축하드립니다.'
        message='다음 주소로 이동하셔서 인증하세요. {}'.format(url)
        html_message=render(self.request, self.email_template_name, {'url':url}).content.decode('utf-8')
        user.email_user(subject, message, settings.EMAIL_HOST_USER, html_message=html_message)
        messages.info(self.request, '회원가입을 축하드립니다. 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.')

    def build_verification_link(self, user, token):
        return '{}/user/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)

class UserVerificationView(TemplateView):
    redirect_url=reverse_lazy('login')
    token_generator=default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            messages.info(request, '인증이 완료되었습니다.')
        else:
            messages.error(request, '인증이 실패되었습니다.')
        return HttpResponseRedirect(self.redirect_url)

    def is_valid_token(self, **kwargs):
        pk=kwargs.get('pk')
        token=kwargs.get('token')
        user=self.model.objects.get(pk=pk)
        is_valid=self.token_generator.check_token(user, token)
        if is_valid:
            user.is_active=True
            user.save()
        return is_valid
