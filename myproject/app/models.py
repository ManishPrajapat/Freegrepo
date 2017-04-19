from django.contrib.auth.models import User
from django.db.models import signals
from tastypie.models import create_api_key
from django.db import models
from django.contrib.gis.db import models as geo_models
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail


def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Blog(BaseModel):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=10000)
    image = models.ImageField(upload_to='blogimage/')

    para1 = models.CharField(max_length=1000,default="",null=True,blank=True)
    image1 = models.ImageField(upload_to='blogimage/',null=True,blank=True)

    para2 = models.CharField(max_length=1000,default="",null=True,blank=True)
    image2 = models.ImageField(upload_to='blogimage/',null=True,blank=True)

    para3 = models.CharField(max_length=1000,default="",null=True,blank=True)
    image3 = models.ImageField(upload_to='blogimage/',null=True,blank=True)

    para4 = models.CharField(max_length=1000,default="",null=True,blank=True)
    image4 = models.ImageField(upload_to='blogimage/',null=True,blank=True)

    para5 = models.CharField(max_length=1000,default="",null=True,blank=True)
    image5 = models.ImageField(upload_to='blogimage/',null=True,blank=True)
    def __unicode__(self):
        return  self.title

class StaticBlogImages(BaseModel):
    blog1 = models.ImageField(upload_to='blogimage/',null=True,blank=True)
    blog2 = models.ImageField(upload_to='blogimage/',null=True,blank=True)
    blog3 = models.ImageField(upload_to='blogimage/', null=True, blank=True)
    blog4 = models.ImageField(upload_to='blogimage/', null=True, blank=True)

    def clean(self):
        validate_only_one_instance(self)

class Casestudy(BaseModel):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=10000)
    image = models.ImageField(upload_to='blogimage/')
    def __unicode__(self):
        return  self.title

class CaseStudyParagraph(BaseModel):
    casestudy = models.ForeignKey(Casestudy)
    paragraph = models.CharField(max_length=4000)
    sequence = models.IntegerField()
    class Meta :
        ordering = ('sequence',)
    def __unicode__(self):
        return self.casestudy.title + "    " + self.paragraph



class HomePageMainHeading(BaseModel):
    heading = models.CharField(max_length=200)
    subheading = models.CharField(max_length=500)
    def __unicode__(self):
        return  self.heading
    def clean(self):
        validate_only_one_instance(self)

class HomePageStatistics1(BaseModel):
    title = models.CharField(max_length=50)
    value = models.IntegerField(default=0)
    def __unicode__(self):
        return  self.title
    def clean(self):
        validate_only_one_instance(self)

class HomePageStatistics2(BaseModel):
    title = models.CharField(max_length=50)
    value = models.IntegerField(default=0)
    def __unicode__(self):
        return  self.title
    def clean(self):
        validate_only_one_instance(self)

class HomePageStatistics3(BaseModel):
    title = models.CharField(max_length=50)
    value = models.IntegerField(default=0)
    def __unicode__(self):
        return  self.title
    def clean(self):
        validate_only_one_instance(self)

class HomePageStatistics4(BaseModel):
    title = models.CharField(max_length=50)
    value = models.IntegerField(default=0)
    def __unicode__(self):
        return  self.title
    def clean(self):
        validate_only_one_instance(self)

class Contact_Form_Success_Steps(BaseModel):
    sequence = models.IntegerField()
    title = models.CharField(max_length=100)
    def __unicode__(self):
        return str(self.sequence) + " " + self.title

    class Meta :
        ordering = ('sequence',)

SECTORDATA = (
        ('Restaurant/Bar/Cafe', 'Restaurant/Bar/Cafe'),
        ('Salon/Spa', 'Salon/Spa'),
        ('Gym', 'Gym'),
        ('Co-working Space', 'Co-working Space'),
        ('Hotel/Resort', 'Hotel/Resort'),
        ('Hospital/Clinic', 'Hospital/Clinic'),
        ('Education', 'Education'),
        ('Retail Mall/Shopping Center', 'Retail Mall/Shopping Center'),
        ('Event', 'Event'),
        ('Marketing/Media Consultant', 'Marketing/Media Consultant'),
        ('Other', 'Other'),
)

class ContactUs(BaseModel):
    name = models.CharField(max_length=200,default="Anonymous")
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=25)
    businessname = models.CharField(max_length=1000,null=True)
    sector = models.CharField(choices=SECTORDATA,max_length=200,null=True)
    address = models.CharField(max_length=1000,null=True)
    officeno = models.CharField(max_length=1000,null=True)
    comments = models.CharField(max_length=1000, null=True)

    def __unicode__(self):
        return self.name

class Query(BaseModel):
    name = models.CharField(max_length=200,default="Anonymous")
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=25)
    businessname = models.CharField(max_length=1000,null=True)
    sector = models.CharField(choices=SECTORDATA,max_length=200,null=True)
    address = models.CharField(max_length=1000,null=True)
    officeno = models.CharField(max_length=1000,null=True)
    comments = models.CharField(max_length=1000, null=True)

    def __unicode__(self):
        return self.name
@receiver(post_save, sender=ContactUs, dispatch_uid="ContactUs")
def update_stock(sender, instance, **kwargs):
    email = instance.email
    contact = instance.contact
    send_mail("Contact Form",email+" "+contact, settings.EMAIL_HOST_USER,
              ['manishhh2108@gmail.com'], fail_silently=False)

@receiver(post_save, sender=Query, dispatch_uid="Query")
def update_stock2(sender, instance, **kwargs):
    email = instance.email
    contact = instance.contact
    send_mail("Query Form",email+" "+contact, settings.EMAIL_HOST_USER,
              ['manishhh2108@gmail.com'], fail_silently=False)

class freegcategory(BaseModel):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100,default="Lorem Ipsum Dolar")
    sequence = models.IntegerField(default=0)
    image = models.ImageField(upload_to='freegcategory/', null=True)
    dashboardimage = models.ImageField(upload_to='freegcategorydashboard/', null=True)
    dashboard_title1 = models.CharField(max_length=100, default="Lorem Ipsum Dolar")
    dashboard_description1 = models.CharField(max_length=500, default="Lorem Ipsum Dolar")
    dashboard_title2 = models.CharField(max_length=100, default="Lorem Ipsum Dolar")
    dashboard_description2 = models.CharField(max_length=500, default="Lorem Ipsum Dolar")
    dashboard_title3 = models.CharField(max_length=100, default="Lorem Ipsum Dolar")
    dashboard_description3 = models.CharField(max_length=500, default="Lorem Ipsum Dolar")
    divider_title1 = models.CharField(max_length=50,default="Lorem Ipsum Dolar")
    divider_description1 = models.CharField(max_length=500, default="Lorem Ipsum Dolar")
    divider_image1 = models.ImageField(upload_to='freegcategory/', null=True)
    divider_title2 = models.CharField(max_length=50,default="Lorem Ipsum Dolar")
    divider_description2 = models.CharField(max_length=500, default="Lorem Ipsum Dolar")
    divider_image2 = models.ImageField(upload_to='freegcategory/', null=True)
    divider_title3 = models.CharField(max_length=50,default="Lorem Ipsum Dolar")
    divider_description3 = models.CharField(max_length=500, default="Lorem Ipsum Dolar")
    divider_image3 = models.ImageField(upload_to='freegcategory/', null=True)
    bottombar = models.CharField(max_length=400,default="Lorem Ipsum")
    bottombarlink = models.CharField(max_length=500,null=True)
    def __unicode__(self):
        return self.title

    class Meta :
        ordering = ('sequence',)

class pricingplan(BaseModel):
    category = models.ForeignKey(freegcategory)
    title = models.CharField(max_length=50)
    price = models.CharField(max_length=12,default=0)
    def __unicode__(self):
        return  self.category.title + "  " +self.title

class pricingplanrow(BaseModel):
    category = models.ForeignKey(freegcategory,null=True)
    title = models.CharField(max_length=50)
    def __unicode__(self):
        return self.category.title + " " + self.title

class pricingplanvalue(BaseModel):
    plan = models.ForeignKey(pricingplan,null=True)
    row = models.ForeignKey(pricingplanrow,null=True)
    value = models.CharField(max_length=100)
    def __unicode__(self):
        return self.row.category.title + " . " + self.plan.title + " . " +self.row.title +" . "+self.value

class Testimonial(BaseModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(freegcategory)
    image = models.ImageField(upload_to='testimonial/', null=True)
    def __unicode__(self):
        return self.name

class Careers(BaseModel):
    position = models.CharField(max_length=200)
    location = models.CharField(max_length=500)
    description = models.CharField(max_length=2000,null=True)
    def __unicode__(self):
        return self.position + "  " + self.location

class Responsibilty(BaseModel):
    career =  models.ForeignKey(Careers)
    title = models.CharField(max_length=200)
    def __unicode__(self):
        return self.title + "  " + self.career.position + " " + self.career.location

class Requirement(BaseModel):
    career = models.ForeignKey(Careers)
    title = models.CharField(max_length=200)
    def __unicode__(self):
        return self.title + "  " + self.career.position + " " + self.career.location

class PerksBenefit(BaseModel):
    career = models.ForeignKey(Careers)
    title = models.CharField(max_length=200)
    def __unicode__(self):
        return self.title + "  " + self.career.position + " " + self.career.location

class Team(BaseModel):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=100,default="Co-Founder")
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='testimonial/', null=True)
    facebook = models.CharField(max_length=250,default="Lorem")
    twitter = models.CharField(max_length=250,default="Lorem")
    linkedin = models.CharField(max_length=250,default="Lorem")
    sequence = models.IntegerField(default=0)
    class Meta :
        ordering = ('sequence',)

    def __unicode__(self):
        return self.name

class FreegInfo(BaseModel):
    logo = models.ImageField(upload_to='logo/', null=True)
    toplogo = models.ImageField(upload_to='logo/', null=True)
    facebook = models.CharField(max_length=250)
    twitter = models.CharField(max_length=250)
    linkedin = models.CharField(max_length=250)
    googleplus = models.CharField(max_length=250)
    instagram = models.CharField(max_length=250)
    saleemailid = models.CharField(max_length=250,default="sales@freeGwifi.com")
    supportemailid = models.CharField(max_length=250,default="support@freeGwifi.com")
    contact = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    longitude = models.CharField(max_length=50,null=True)
    latitude = models.CharField(max_length=50,null=True)
    aboutfreegwifi = models.CharField(max_length=1000,default="Lorem Ipsum Model.py Lorem Ipsum Model.py Lorem Ipsum Model.py Lorem Ipsum Model.py Lorem Ipsum Model.py ")
    loginlink = models.CharField(max_length=200,default="#")
    def clean(self):
        validate_only_one_instance(self)

class HomePagebackgroundimage(BaseModel):
    homepage = models.ImageField(upload_to='largebackground/', null=True)
    def clean(self):
        validate_only_one_instance(self)

class HomePageCaseStudy(BaseModel):
    image = models.ImageField(upload_to='homepagecasestudy/', null=True)
    venue = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    def clean(self):
        validate_only_one_instance(self)

class ContactPageCaseStudy(BaseModel):
    image = models.ImageField(upload_to='homepagecasestudy/', null=True)
    venue = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    def clean(self):
        validate_only_one_instance(self)

class BestClinetsImages(BaseModel):
    image = models.ImageField(upload_to='bestclinets/', null=True)

class Freegheadquaters(BaseModel):
    cityname = models.CharField(max_length=100)
    contact = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    sequence = models.IntegerField(default=0)
    location = models.CharField(max_length=250)
    longitude = models.CharField(max_length=15)
    latitude = models.CharField(max_length=15)
    def clean(self):
        validate_only_one_instance(self)

    def __unicode__(self):
        return self.cityname

class BranchOffices(BaseModel):
    cityname = models.CharField(max_length=100)
    contact = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    sequence = models.IntegerField(default=0)
    class Meta :
        ordering = ('sequence',)

    def __unicode__(self):
        return self.cityname

class ChannelPartners(BaseModel):
    cityname = models.CharField(max_length=100)
    contact = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    sequence = models.IntegerField(default=0)
    class Meta :
        ordering = ('sequence',)

    def __unicode__(self):
        return self.cityname

class HowFreegCanHelp(BaseModel):
    divider_title1 = models.CharField(max_length=50, default="Lorem Ipsum Dolar")
    divider_description1 = models.CharField(max_length=500, default="Lorem Ipsum Dolar")
    divider_image1 = models.ImageField(upload_to='freegcategory/', null=True)
    divider_title2 = models.CharField(max_length=50, default="Lorem Ipsum Dolar")
    divider_description2 = models.CharField(max_length=500, default="Lorem Ipsum Dolar")
    divider_image2 = models.ImageField(upload_to='freegcategory/', null=True)
    divider_title3 = models.CharField(max_length=50, default="Lorem Ipsum Dolar")
    divider_description3 = models.CharField(max_length=500, default="Lorem Ipsum Dolar")
    divider_image3 = models.ImageField(upload_to='freegcategory/', null=True)
    def clean(self):
        validate_only_one_instance(self)

class FormSuccess(BaseModel):
    title1 = models.CharField(max_length=50, default="Lorem Ipsum Dolar")
    description1 = models.CharField(max_length=500, default="Lorem Ipsum Dolar")
    title2 = models.CharField(max_length=50, default="Lorem Ipsum Dolar")
    description2 = models.CharField(max_length=500, default="Lorem Ipsum Dolar")
    title3 = models.CharField(max_length=50, default="Lorem Ipsum Dolar")
    divider_description3 = models.CharField(max_length=500, default="Lorem Ipsum Dolar")
    def clean(self):
        validate_only_one_instance(self)

class CareerForm(BaseModel):
    name = models.CharField(max_length=200, default="Anonymous")
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=25)
    position = models.CharField(max_length=100)
    resume = models.FileField(upload_to='documents/%Y/%m/%d',null=True)
    tellus = models.CharField(max_length=1000,null=True)
    def __unicode__(self):
        return self.name
@receiver(post_save, sender=CareerForm, dispatch_uid="CareerForm")
def update_stock3(sender, instance, **kwargs):
    email = instance.email
    contact = instance.contact
    send_mail("CareerForm Form",email+" "+contact, settings.EMAIL_HOST_USER,
              ['manishhh2108@gmail.com'], fail_silently=False)

class CareerOtherForm(BaseModel):
    name = models.CharField(max_length=200, default="Anonymous")
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=25)
    resume = models.FileField(upload_to='documents/%Y/%m/%d',null=True)
    tellus = models.CharField(max_length=1000, null=True)
    def __unicode__(self):
        return self.name

@receiver(post_save, sender=CareerOtherForm, dispatch_uid="CareerOtherForm")
def update_stock4(sender, instance, **kwargs):
    email = instance.email
    contact = instance.contact
    send_mail("CareerOtherForm Form",email+" "+contact, settings.EMAIL_HOST_USER,
              ['manishhh2108@gmail.com'], fail_silently=False)

class MoreCategories(BaseModel):
    title = models.CharField(max_length=200)
    sequence = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    class Meta :
        ordering = ('sequence',)

class MoreCategorySubCategory(BaseModel):
    morecategory = models.ForeignKey(MoreCategories)
    title = models.CharField(max_length=200)
    sequence = models.IntegerField(default=0)
    image = models.ImageField(upload_to='MoreCategorySubCategory/')
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ('sequence',)

class AboutUs_How_We_Started(BaseModel):
    content = models.CharField(max_length=4000)
    sequence = models.IntegerField()

    class Meta:
        ordering = ('sequence',)
    def __unicode__(self):
        return self.content

class AboutUs_Our_Vision(BaseModel):
    content = models.CharField(max_length=4000)
    sequence = models.IntegerField()

    class Meta:
        ordering = ('sequence',)
    def __unicode__(self):
        return self.content

class AboutUs_What_We_Do(BaseModel):
    title = models.CharField(max_length=100,null=True)
    content = models.CharField(max_length=4000)
    image = models.ImageField(upload_to='blogimage/')
    sequence = models.IntegerField()

    class Meta:
        ordering = ('sequence',)
    def __unicode__(self):
        return self.content