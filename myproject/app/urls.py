from django.conf.urls import url
from app import views

app_name = "app"
urlpatterns = [
    url(r'^$', views.homepage, name="homepage"),
    url(r'^index/$', views.homepage, name="homepage"),
    url(r'^contact/$', views.contact, name="contact"),
    url(r'^courses/(?P<id>\d+)/$', views.courses, name="courses"),
    url(r'^pricing/$', views.pricing, name="pricing"),
    url(r'^team/$', views.team, name="team"),
    url(r'^contactus$', views.contactus, name="contactus"),
    url(r'^blog/$', views.blog, name="blog"),
    url(r'^singleblog/(?P<id>\d+)/$', views.singleblog, name="singleblog"),
    url(r'^casestudy/$', views.casestudy, name="casestudy"),
    url(r'^singlecasestudy/(?P<id>\d+)/$', views.singlecasestudy, name="singlecasestudy"),
]
