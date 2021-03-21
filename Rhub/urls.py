from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [

    # Setting url paths for website.
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('movies/', views.movies, name="movies"),
    path('series/', views.series, name="series"),
    path('movies/<movie_id>/', views.singleMovie,name="singleMovie"),
    path('series/<series_id>/', views.singleSeries, name="singleSeries"),
    path('register/', views.register, name = "register"),
    path('profile/', views.profile, name = "user_profile"),

    #Changing Password Urls.
    path('change-password/', 
    auth_views.PasswordChangeView.as_view(template_name="common\change-password.html", success_url="/change-password-done/"),
    name = "change_password"),
    path('change-password-done/',
    auth_views.PasswordChangeDoneView.as_view(template_name="common\change-password-done.html"),
    name="change_password_done"),

    #Reset Password Urls.
    path('password-reset/',
    auth_views.PasswordResetView.as_view(template_name="common\password-reset.html", subject_template_name="common\password-reset-text.txt", email_template_name="common\password_reset_email.html", success_url="/password-reset/done/"),
    name="reset_password"),
    path('password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(template_name="common\password-reset-sent.html"),
    name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="common\password-reset-confirm.html", success_url="/password-reset-complete/"),
    name="passwordresetconfirm"),
    path('password-reset-complete/',
    auth_views.PasswordResetDoneView.as_view(template_name="common\password-reset-complete.html"),
    name="password_reset_complete"),
    
]

'''
Urls of change password.
1. Change password Form         //PasswordChangeView.as_view()
2. Change password done         //PasswordChangeDoneView.as_view()
'''

'''
The last for urls are to reset password, I am using django authentication module views here.
1. Submit email Form                        //PasswordResetView.as_view()
2. Email sent success message               //PasswordResetDoneView.as_view()
3. Link to password Reset form in email     //PasswordResetConfirmView.as_view()
4. Password successfully changed message    //PasswordRestCompleteView.as_view()
'''