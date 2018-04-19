
from django.conf.urls import url 
from . import views 
 
urlpatterns = [ 
    url(r'^$', views.index), 
    url(r'^validate$', views.validate), 
    url(r'^login$', views.login), 
    url(r'^dashboard$', views.dashboard), 
    url(r'^results$', views.results), 
    url(r'^user/(?P<id>\d+)$', views.showUser, name='user_id'), 
    url(r'^user/(?P<id>\d+)/edit$', views.editUser, name='edit_user_id'),
    url(r'^user/(?P<id>\d+)/update$', views.update),
    url(r'^user/(?P<id>\d+)/upload$', views.upload),
    url(r'^post/(?P<id>\d+)$', views.showPost, name='post_id'), 
    url(r'^add$', views.addPost),
    url(r'^post/(?P<id>\d+)/comment$', views.comment),
    url(r'^(?P<id>\d+)/comment$', views.comment),
    url(r'^(?P<id>\d+)/delete$', views.deletepost),
    url(r'^post/comment/(?P<id>\d+)/delete$', views.deletecomment),
    url(r'^comment/(?P<id>\d+)/delete$', views.deletecomment),
    url(r'^page1$', views.page1),
    url(r'^page2$', views.page2),
    url(r'^page3$', views.page3),
    url(r'^page4$', views.page4),
    url(r'^page5$', views.page5),
    url(r'^user/(?P<id>\d+)/awards$', views.awards),
    url(r'^post/(?P<id>\d+)/uploadfile$', views.uploadfile),
] 