from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from .models import MyUser
from .utils.mailer import send_html_mail


class ForgotRestPasswordView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'forgot.html')

    def post(self, request, *args, **kwargs):

        email = request.POST.get('email')
        if email:
            try:
                user_ = MyUser.objects.get(email=email)

                token = account_activation_token.make_token(user_)

                url_ = request.build_absolute_uri(reverse_lazy(
                    'ac:reset-password',
                    args=(
                        str(token),
                        urlsafe_base64_encode(force_bytes(user_.email)),)
                ))
                link = f"""<a href="{url_}" target="_blank">Reset</a>"""

                send_html_mail(
                    "Reset-Password",
                    f"""<h1>Click on link to reset password</h1> <br/> {link}""",
                    recipient_list=[str(user_.email), ]
                )

                messages.success(
                    request, 'A link has been send to your email!')
                return redirect('ac:login')
            except:
                messages.error(
                    request, 'No user found!')
                return render(request, 'forgot.html')

        messages.error(request, ''' Something went wrong to sending email! ''')
        return render(request, 'forgot.html')


def rest_password(request, token, email):

    try:
        user = MyUser.objects.get(
            email=force_str(urlsafe_base64_decode(email)))
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
        return render(request, 'forgot_reset_part/invalid.html')

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            password1 = request.POST.get("pwd")
            password2 = request.POST.get("pwd2")
            if password1 == password2:
                user.set_password(str(password2))
                user.save()
                return render(request, 'forgot_reset_part/message_reset.html')

            return render(request, 'forgot_reset_part/forms-re.html')

        return render(request, 'forgot_reset_part/forms.html')

    return render(request, 'forgot_reset_part/invalid.html')
