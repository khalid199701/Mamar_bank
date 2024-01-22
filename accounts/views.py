from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import login,logout
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth import login, update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.
# def pass_change(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, data = request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Password Updated Successfully')
#             update_session_auth_hash(request, form.user)
#             return redirect('accounts/profile.html')
    
#     else:
#         form = PasswordChangeForm(user = request.user)
#     return render(request, 'accounts/pass_change.html', {'form': form})

class PasswordChangeView(FormView):
    template_name = 'accounts/pass_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Password Updated Successfully')
        update_session_auth_hash(self.request, form.user)
        mail_subject = 'Password Change'
        message = render_to_string('accounts/pass_email.html',{
            'user': self.request.user
        })
        to_email = self.request.user.email
        send_email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
        send_email.attach_alternative(message, 'text/html')
        send_email.send()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
        
class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})