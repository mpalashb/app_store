from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, DeleteView, UpdateView, ListView
from django.contrib.auth import authenticate, login, mixins, views, models
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import MyUser
from apps_app.models import LargeImages, AppProduct
from users.profileModels import ProfileModel
from .forms.registerForms import UserCreationFormExtend
from .forms.loginForms import LoginForm
from .forms.uploadForms import UploadAppForm
from .forms.profileForms import ProfileForms


class UploadView(mixins.LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'ac:login'
    redirect_field_name = 'next'
    success_url = reverse_lazy("ac:current-user", current_app='users')
    success_message = 'Uploaded successfully!'
    form_class = UploadAppForm
    template_name = 'upload-app.html'

    def form_invalid(self, form):
        messages.error(
            self.request, f'Error uploading..., check the fields {form.errors.as_text()}')
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        apps_saved = super().form_valid(form)

        large_img_files = self.request.FILES.getlist(
            'all_large_images') or None
        if large_img_files:
            for img in large_img_files:
                large_img_inc = LargeImages(
                    product_id=form.instance,
                    img=img
                )
                large_img_inc.save()

        return apps_saved


class DashboardView(mixins.LoginRequiredMixin, View):
    login_url = 'ac:login'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwarg):
        return render(request, 'dashboard.html')


class RegisterView(View):
    form_class = UserCreationFormExtend

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form, 'message': None}
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account registered!')
            return redirect('ac:login')

        messages.error(request, 'Register failed!')
        message = 'Register failed!'
        context = {'form': form, 'message': message}
        return render(request, 'register.html', context)


class LogoutViewExtend(views.LogoutView):
    next_page = 'ac:login'


class LoginView(View):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        context = {'form': form, 'message': message}
        return render(request, 'login.html', context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login success!')
                if user.is_admin:
                    return redirect('admin:index')
                return redirect('ac:current-user')

        # print(request.POST.get('email'))

        messages.error(request, 'Login failed!')
        message = 'Login failed!'
        context = {'form': form, 'message': message}
        return render(request, 'login.html', context)


class ProfileCreate(mixins.LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'ac:login'
    redirect_field_name = 'next'
    success_url = reverse_lazy("ac:current-user", current_app='users')
    success_message = 'Profile Created!'
    form_class = ProfileForms
    template_name = 'profile-form.html'

    def form_invalid(self, form):
        messages.error(
            self.request, f'Error Profile creating..., check the fields {form.errors.as_text()}')
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.user_ac = self.request.user

        return super().form_valid(form)


class DeleteProfile(mixins.LoginRequiredMixin, View):
    model = ProfileModel
    login_url = reverse_lazy('ac:login', current_app='users')
    redirect_field_name = 'next'
    success_url = reverse_lazy("ac:current-user", current_app='users')
    success_message = 'Profile Deleted!'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        current_user.profile.delete()
        messages.warning(request, self.success_message)
        return redirect('ac:current-user')


class UpdateProfile(mixins.LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ProfileModel
    template_name = 'profile-form-update.html'
    login_url = reverse_lazy('ac:login', current_app='users')
    redirect_field_name = 'next'
    form_class = ProfileForms
    success_url = reverse_lazy("ac:current-user", current_app='users')
    success_message = 'Profile Updated!'

    pk_url_kwarg = "profile_pk"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user_ac != self.request.user:
            messages.warning(
                request, '''Owner permission is required!''')
            return redirect('ac:current-user')

        return super().dispatch(request, *args, **kwargs)

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     if self.request.method == "post" or "POST":
    #         context['form'] = self.get_form()


class DeleteAccount(mixins.LoginRequiredMixin, DeleteView):
    model = MyUser
    login_url = reverse_lazy('ac:login', current_app='users')
    redirect_field_name = 'next'
    success_url = reverse_lazy("ac:login", current_app='users')

    def post(self, request, *args, **kwargs):
        request.user.delete()
        messages.error(request, "Account permanently deleted!")
        return redirect('ac:login')


class OwnerUploadApps(mixins.LoginRequiredMixin, ListView):
    model = AppProduct
    template_name = "owner-apps.html"
    login_url = reverse_lazy('ac:login', current_app='users')
    redirect_field_name = 'next'
    ordering = "-pk"

    def get_queryset(self):
        custom_query = self.request.user.all_apps
        if not custom_query.all():
            self.extra_context = {
                'apps_list_owner': custom_query.all(), 'msg': "No apps uploaded yet!"}
        else:
            self.extra_context = {
                'apps_list_owner': custom_query.all(), 'msg': None}
        return custom_query


class OwnerUploadedAppsUpdate(mixins.LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AppProduct
    form_class = UploadAppForm
    template_name = "update-app.html"
    login_url = reverse_lazy('ac:login', current_app='users')
    redirect_field_name = 'next'
    success_url = reverse_lazy("ac:owner-apps", current_app='users')
    success_message = 'Apps Updated!'

    slug_url_kwarg = "apps_slug"

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        obj = self.get_object()
        self.extra_context = {'slug': obj.slug}

        if obj.author != current_user:
            messages.error(request, 'Owner permission is required!')
            return redirect("ac:owner-apps")

        large_img_files = self.request.FILES.getlist(
            'all_large_images') or None
        if large_img_files:
            try:
                get_inc = LargeImages.objects.filter(
                    product_id=obj,
                )
                get_inc.all().delete()
            except:
                messages.error(request, '''Can't updateed large images!''')

            for img in large_img_files:
                large_img_inc = LargeImages(
                    product_id=obj,
                )
                large_img_inc.img = img
                large_img_inc.save()

        return super().dispatch(request, *args, **kwargs)


class OwnerUploadedAppsDelete(mixins.LoginRequiredMixin, DeleteView):
    model = AppProduct
    login_url = reverse_lazy('ac:login', current_app='users')
    redirect_field_name = 'next'
    success_url = reverse_lazy("ac:owner-apps", current_app='users')
    slug_url_kwarg = "apps_slug"

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        obj = self.get_object()

        if obj.author != current_user:
            messages.error(request, 'Owner permission is required!')
            return redirect("ac:owner-apps")

        if request.POST:
            obj.delete()
            messages.warning(request, 'Apps deleted!')
            return redirect("ac:owner-apps")

        return super().dispatch(request, *args, **kwargs)
