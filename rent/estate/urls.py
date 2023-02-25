from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path
from django.urls import reverse_lazy
from django.conf import settings
from . import views
from estate.views import UserLoginAdd, UserLoginFavorite, UserLoginChat

AuthenticationForm.my_extra_data = 'foobar'

LOGIN_URL = reverse_lazy('login_view', kwargs={'parameter': 'login_parameter'})

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', auth_views.LoginView.as_view(template_name = 'estate/login.html'), name = 'login'),
    path('login_warning/', UserLoginAdd.as_view(), name="login_warning_add"),
    path('login_warning_favorite/', UserLoginFavorite.as_view(), name="login_warning_favorite"),
    path('login_warning_chat/', UserLoginChat.as_view(), name="login_warning_chat"),
    #path('login/<str:warning>', auth_views.LoginView.as_view(template_name = 'estate/login.html'), name = 'login'),
    #path('login/', 'django.contrib.auth.views.login',
    # {'template_name': 'estate/login.html',
    #  'authentication_form': AuthenticationForm }),
    path('register/', views.register, name='register'),
    path('add_post/(?P<warning>\d+)', views.add_post, name='add_post'),
    path('registered/', views.registered, name='registered'),
    path('logout_view/', views.logout_view, name='logout_view'),
    #path('reset_password/', views.password_reset_request, name='password_reset_request'),
    #path('confirm_reset/', views.confirm_reset, name='confirm_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='estate/password_reset_done.html'), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='estate/password_reset_confirm.html'), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='estate/password_reset_complete.html'), name='password_reset_complete'),
    path('change_data/', views.change_data, name='change_data'),
    path('back/', views.back, name='back'),
    path('account/', views.account, name='account'),
    path('annoucement_item/<int:arg>', views.annoucement_item, name='annoucement_item'),
    path('favorite/', views.favorite, name='favorite'),
    path('add_post/', views.add_post, name='add_post'),
    path('add_favorite/<int:arg>', views.add_favorite, name='add_favorite'),
    path('add_favorite_from_main/<int:arg>', views.add_favorite_from_main, name='add_favorite_from_main'),
    path('remove_favorite/<int:arg>', views.remove_favorite, name='remove_favorite'),
    path('add_compilation', views.add_compilation, name='add_compilation'),
    path('remove_compilation/<int:arg>', views.remove_compilation, name='remove_compilation'),
    path('save_compilation/<int:arg>', views.save_compilation, name='save_compilation'),
    path('add_in_compilation', views.add_in_compilation, name='add_in_compilation'),
    path('show_compilation/<int:arg>', views.show_compilation, name='show_compilation'),
    path('adding/', views.adding, name='adding'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('flats/', views.flats, name='flats'),
    path('houses/', views.houses, name='houses'),
    path('rooms/', views.rooms, name='rooms'),
    path('searched/', views.searched, name='searched'),
    path('chat/', views.chat, name='chat'),
    path('open_chat', views.open_chat, name='open_chat'),
    path('open_chat/<int:arg>', views.open_chat, name='open_chat'),
    path('change_chat/<int:chat>', views.change_chat, name='change_chat'),
    path('change_chat/<int:chat>/<int:arg>', views.change_chat, name='change_chat'),
    path('send_first_message/<str:arg>', views.send_first_message, name='send_first_message'),
    path('send_message/<int:chat>', views.send_message, name='send_message'),
    path('send_message/<int:chat>/<int:arg>', views.send_message, name='send_message'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="estate/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="estate/password_reset_send.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="estate/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="estate/password_reset_complete.html"), name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
