from django.urls import path
from . import views
from .views import delete_post, course_detail

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('community/', views.community, name='community'),
    path('news/', views.news, name='news'),
    path('learn/', views.learn, name='learn'),
    path('add_post/', views.add_post, name='add_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('redirect_to_index/', views.redirect_to_index, name='redirect_to_index'),
     path('mark-completed/<int:video_id>/', views.mark_completed, name='mark_completed'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





