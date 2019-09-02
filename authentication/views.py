from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import User
from .forms import ChatUserCreationForm
from .models import User
from .tokens import account_activation_token


# Create your views here.
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'cauth2/activation_invalid.html')


def activation_email_sent(request):
    return render(request, 'cauth2/confirm_email.html')


def signup(request):
    if request.method == 'POST':
        form = ChatUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('cauth2/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return redirect('accounts:activation_email_sent')
        else:
            form = ChatUserCreationForm()
        return render(request, 'cauth2/signup.html', {'form': form})
    else:
        form = ChatUserCreationForm()
    return render(request, 'cauth2/signup.html', {'form': form})