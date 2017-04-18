from django.conf.urls import url
from app import views

app_name = "app"
urlpatterns = [
    url(r'^$', views.homepage, name="homepage"),
    url(r'^index/$', views.homepage, name="homepage"),
    url(r'^contact/$', views.contact, name="contact"),
    url(r'^contact2/$', views.contact2, name="contact2"),
    url(r'^courses/(?P<id>\d+)/$', views.courses, name="courses"),
    url(r'^pricing/$', views.pricing, name="pricing"),
    url(r'^team/$', views.team, name="team"),
    url(r'^aboutus/$', views.aboutus, name="aboutus"),
    url(r'^career/$', views.career, name="career"),
    url(r'^contactus/$', views.contactus, name="contactus"),
    url(r'^contactus2/$', views.contactus2, name="contactus2"),
    url(r'^blog/$', views.blog, name="blog"),
    url(r'^morecategory/$', views.morecategory, name="morecategory"),
    url(r'^formsuccess', views.formsuccess, name="formsuccess"),
    url(r'^careerfinal', views.careerfinal, name="careerfinal"),
    url(r'^careerdetail/(?P<id>\d+)/$', views.careerdetail, name="careerdetail"),
    url(r'^formcareer/(?P<id>\d+)/$', views.formcareer, name="formcareer"),
    url(r'^cformsubmit/$', views.cformsubmit, name="cformsubmit"),
    url(r'^cotherformsubmit/$', views.cotherformsubmit, name="cotherformsubmit"),
    url(r'^singleblog/(?P<id>\d+)/$', views.singleblog, name="singleblog"),
    url(r'^singleblog1/$', views.singleblog1, name="singleblog1"),
    url(r'^singleblog2/$', views.singleblog2, name="singleblog2"),
    url(r'^singleblog3/$', views.singleblog3, name="singleblog3"),
    url(r'^singleblog4/$', views.singleblog4, name="singleblog4"),
    url(r'^casestudy/$', views.casestudy, name="casestudy"),
    url(r'^singlecasestudy/(?P<id>\d+)/$', views.singlecasestudy, name="singlecasestudy"),
]
