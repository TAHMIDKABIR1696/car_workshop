from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from . import views

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

urlpatterns = [
    # app_auth views ::
    path('', views.home, name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name="register"),
    path('appointment-form/', views.appointment_form, name="appointment_form"),
    path('register-submit', views.register_submit, name='register_submit'),
    path('appointment_list/', views.appointment_list, name="appointment_list"),
    path('check-availability/', views.check_mechanic_availability, name='check_availability'),
    path('submit_appointment/', views.submit_appointment, name="submit_appointment"),
    path('update_appointment/<int:id>/', views.update_appointment, name='update_appointment'),
    path('get_available_mechanics/', views.get_available_mechanics, name='get_available_mechanics'),
    path('mechanic_list/', views.mechanic_list, name="mechanic_list"),
    path('client_list/', views.client_list, name="client_list"),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)