from django.urls import path
from . import views
from .views import delete_post
from .views import course_detail 
urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('community/', views.community, name='community'),
    path('markets/', views.markets, name='markets'),
    path('news/', views.news, name='news'),
    path('broker/', views.broker, name='broker'),
    path('learn/', views.learn, name='learn'),
    path('add_post/', views.add_post, name='add_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




