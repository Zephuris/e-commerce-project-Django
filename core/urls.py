from django.urls import path,include
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('register/', views.register_view),
    path('login/',views.loginView),
    path('dashboard',views.DashbordView),
    path('profile-edit/',views.ProfileView),
    path('logout/',views.logoutView),
    path('change-password/',views.passwordEditView),
]
