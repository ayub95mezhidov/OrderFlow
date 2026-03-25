from django.urls import path

from .views import (login, registration, profile, logout,
                    CustomPasswordResetView, CustomPasswordResetDoneView,
                    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView)

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]