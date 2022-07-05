from django.urls import path

from users.views import (
    RegisterView, DashboardView, LoginView,
    LogoutViewExtend, UploadView, ProfileCreate,
    DeleteProfile, DeleteAccount, UpdateProfile,
    OwnerUploadApps, OwnerUploadedAppsDelete, OwnerUploadedAppsUpdate,

)

from .passwordReset import rest_password, ForgotRestPasswordView

app_name = 'users'

urlpatterns = [
    path('owner_apps/<str:apps_slug>/edit',
         OwnerUploadedAppsUpdate.as_view(), name='owner-apps-update'),
    path('owner_apps/<str:apps_slug>/delete',
         OwnerUploadedAppsDelete.as_view(), name='owner-apps-delete'),
    path('owner_apps/all', OwnerUploadApps.as_view(), name='owner-apps'),
    path('delete', DeleteAccount.as_view(), name='ac-delete'),
    path('user/profile/delete', DeleteProfile.as_view(), name='profile-delete'),
    path('user/profile/edit/<int:profile_pk>',
         UpdateProfile.as_view(), name='profile-update'),
    path('user/profile/create', ProfileCreate.as_view(), name='profile-create'),
    path('user/upload', UploadView.as_view(), name='upload'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutViewExtend.as_view(), name='logout'),
    path('user/me', DashboardView.as_view(), name='current-user'),
]

urlpatterns += [
    path('forgot-reset', ForgotRestPasswordView.as_view(), name='forgot'),
    path('forgot-password-reset/<str:token>/<str:email>',
         rest_password, name="reset-password"),
]
