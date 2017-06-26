from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re
from app.models import *
import json
from datetime import datetime
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import render_to_response
from django.template import RequestContext


def homepage(request):
    context = {}

    #MetaData
    MetaDataAllobj = MetaDataAll.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    singlemetadata = MetaDataAllobj.homepage
    context['metadata_author'] = singlemetadata.author
    context['metada_description'] = singlemetadata.description
    context['metadata_keywords'] = singlemetadata.keywords

    #Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]
    
    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url
    
    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_play'] = Favicons.play.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    #title
    titleobj = WebsiteTitles.objects.all()
    titleobj = titleobj[0]
    homepage = titleobj.homepage
    context['pagetitle'] = homepage

    #HomePageMainHeading data
    HomePageMainHeadingobj = HomePageMainHeading.objects.all()
    HomePageMainHeadingobj = HomePageMainHeadingobj[0]
    context['heading'] = HomePageMainHeadingobj.heading
    context['subheading'] = HomePageMainHeadingobj.subheading

    # BestClientData
    bestclient = []
    allbestclient = BestClinetsImages.objects.all()
    for singlebestclient in allbestclient:
        bestclient.append(singlebestclient.image.url)
    context['bestclient'] = bestclient

    #backgroudn image r than life
    bgobj = HomePagebackgroundimage.objects.all()
    bgobj = bgobj[0]
    context['mainbackground'] = bgobj.homepage.url

    #BestClientData
    bestclient = []
    allbestclient = BestClinetsImages.objects.all()
    for singlebestclient in allbestclient:
        bestclient.append(singlebestclient.image.url)
    context['bestclient'] = bestclient
    # branch office data
    branchdata = []
    BranchOfiicesObj =  BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city' : singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata

    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata


    #How freeg wifi can help you
    freegwifiHelpObj = HowFreegCanHelp.objects.all()
    freegwifiHelpObj = freegwifiHelpObj[0]
    context['category_divider_title1'] = freegwifiHelpObj.divider_title1
    context['category_divider_description1'] = freegwifiHelpObj.divider_description1
    context['category_divider_image1'] = freegwifiHelpObj.divider_image1.url
    context['category_divider_title2'] = freegwifiHelpObj.divider_title2
    context['category_divider_description2'] = freegwifiHelpObj.divider_description2
    context['category_divider_image2'] = freegwifiHelpObj.divider_image2.url
    context['category_divider_title3'] = freegwifiHelpObj.divider_title3
    context['category_divider_description3'] = freegwifiHelpObj.divider_description3
    context['category_divider_image3'] = freegwifiHelpObj.divider_image3.url

    #home page statistics data
    stats1 = HomePageStatistics1.objects.all()
    stats2 = HomePageStatistics2.objects.all()
    stats3 = HomePageStatistics3.objects.all()
    stats4 = HomePageStatistics4.objects.all()
    stats1 = stats1[0]
    stats2 = stats2[0]
    stats3 = stats3[0]
    stats4 = stats4[0]

    statlist =[]
    statvaluelist =[]

    statlist.append(stats1.title)
    statvaluelist.append(stats1.value)

    statlist.append(stats2.title)
    statvaluelist.append(stats2.value)

    statlist.append(stats3.title)
    statvaluelist.append(stats3.value)

    statlist.append(stats4.title)
    statvaluelist.append(stats4.value)

    statsdata = zip(statlist,statvaluelist)
    context['statsdata'] = statsdata

    #Case study data
    casestudy_model = HomePageCaseStudy.objects.all()
    casestudy_model = casestudy_model[0]
    context['casestudy_image'] = casestudy_model.image.url
    context['casestudy_venue'] = casestudy_model.venue
    context['casestudy_description'] = casestudy_model.description

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id' : singlecategory.id,
            'title' : singlecategory.title,
            'image' : singlecategory.image.url,
            'showcase_diversity_image' :singlecategory.showcase_diversity_image.url
        })
    context['freegcategory'] = freegcategorieslist

    # testimonial data
    testlist = []
    testimonials = Testimonial.objects.all()
    testimonials = testimonials[0:3]
    for singletest in testimonials:
        testlist.append({
            'name' : singletest.name,
            'description' : singletest.description,
            'image' : singletest.image.url
        })
    context['testimonial'] = testlist

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    #freegwifi google facebook data
    try :
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['video'] = freeginfo.video
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['instagram'] = freeginfo.instagram
        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink

        context['copyrighttext'] = freeginfo.copyrighttext
        context['showcase_of_our_diversity_text'] = freeginfo.showcase_of_our_diversity_text


    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/index.html',context=context)

@csrf_exempt
def cformsubmit(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        position = request.POST['position']
        resume = request.FILES['resume']
        tellus = request.POST['tellus']
        cf = CareerForm(name=name,email=email,contact=contact,position=position,resume=resume,tellus=tellus)
        cf.save()
        return HttpResponseRedirect('/careerfinal/')

@csrf_exempt
def cotherformsubmit(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        tellus = request.POST['tellus']
        resume = request.FILES['resume']
        cf = CareerOtherForm(name=name,email=email,contact=contact,resume=resume,tellus=tellus)
        cf.save()
        return HttpResponseRedirect('/careerfinal/')

@csrf_exempt
def contactus(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        email = email.strip('')
        contact = request.POST['contact']
        sector = request.POST['sector']
        businessname = request.POST['businessname']
        address = request.POST['address']
        officeno = request.POST['officeno']
        comments = request.POST['comments']
        contact_obj = ContactUs(name=name,email=email, contact=contact,comments=comments,
                                businessname=businessname, sector=sector, address=address, officeno=officeno)
        contact_obj.save()


        return HttpResponseRedirect('/formsuccess')

@csrf_exempt
def contactus2(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        sector = request.POST['sector']
        businessname = request.POST['businessname']
        address = request.POST['address']
        officeno = request.POST['officeno']
        comments = request.POST['comments']
        contact_obj = Query(name=name,email=email, contact=contact,comments=comments,
                                businessname=businessname, sector=sector, address=address, officeno=officeno)
        contact_obj.save()

        return HttpResponseRedirect('/formsuccess')

def contact(request):
    context = {}

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    # MetaData
    MetaDataAllobj = MetaDataAll.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    singlemetadata = MetaDataAllobj.contact
    context['metadata_author'] = singlemetadata.author
    context['metada_description'] = singlemetadata.description
    context['metadata_keywords'] = singlemetadata.keywords

    # title
    titleobj = WebsiteTitles.objects.all()
    titleobj = titleobj[0]
    contact = titleobj.contact
    context['pagetitle'] = contact

    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    bgimage = bgimageobj.contact_image.url
    context['bgimage'] = bgimage

    # How freeg wifi can help you
    freegwifiHelpObj = HowFreegCanHelp.objects.all()
    freegwifiHelpObj = freegwifiHelpObj[0]
    context['category_divider_title1'] = freegwifiHelpObj.divider_title1
    context['category_divider_description1'] = freegwifiHelpObj.divider_description1
    context['category_divider_image1'] = freegwifiHelpObj.divider_image1.url
    context['category_divider_title2'] = freegwifiHelpObj.divider_title2
    context['category_divider_description2'] = freegwifiHelpObj.divider_description2
    context['category_divider_image2'] = freegwifiHelpObj.divider_image2.url
    context['category_divider_title3'] = freegwifiHelpObj.divider_title3
    context['category_divider_description3'] = freegwifiHelpObj.divider_description3
    context['category_divider_image3'] = freegwifiHelpObj.divider_image3.url

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata

    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # static blog images
    StaticBlogImagesobj = StaticBlogImages.objects.all()
    StaticBlogImagesobj = StaticBlogImagesobj[0]
    context['blog1image'] = StaticBlogImagesobj.blog1.url
    context['blog2image'] = StaticBlogImagesobj.blog2.url
    context['blog3image'] = StaticBlogImagesobj.blog3.url
    context['blog4image'] = StaticBlogImagesobj.blog4.url

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist
    #BestClientData
    bestclient = []
    allbestclient = BestClinetsImages.objects.all()
    allbestclient = allbestclient[:4]
    for singlebestclient in allbestclient:
        bestclient.append(singlebestclient.image.url)
    context['bestclient'] = bestclient

    # Case study data
    casestudy_model = ContactPageCaseStudy.objects.all()
    casestudy_model = casestudy_model[0]
    context['casestudy_image'] = casestudy_model.image.url
    context['casestudy_venue'] = casestudy_model.venue
    context['casestudy_description'] = casestudy_model.description

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # Allblogs data
    allBlogs = Blog.objects.all()
    bloglist = []
    counter = 0
    for singleBlog in allBlogs:
        if counter < 3:
            bloglist.append({
                'id': singleBlog.id,
                'title': singleBlog.title,
                'content': singleBlog.content,
                'image': singleBlog.image.url,
                'date': singleBlog.created_at
            })
            counter = counter + 1
    context['allblogs'] = bloglist
    #headquaters data
    headlist =[]
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname' : singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    #choicedata
    choicedata = []
    choicesall = ContactUs._meta.get_field('sector').choices
    for singlech in choicesall:
        choicedata.append(list(singlech)[0])
    context['choice'] = choicedata

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['instagram'] = freeginfo.instagram
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext


    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/contact.html',context=context)

def contact2(request):
    context = {}

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    bgimage = bgimageobj.contact_image.url
    context['bgimage'] = bgimage

    # title
    titleobj = WebsiteTitles.objects.all()
    titleobj = titleobj[0]
    contact = titleobj.contact
    context['pagetitle'] = contact

    # MetaData
    MetaDataAllobj = MetaDataAll.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    singlemetadata = MetaDataAllobj.contact
    context['metadata_author'] = singlemetadata.author
    context['metada_description'] = singlemetadata.description
    context['metadata_keywords'] = singlemetadata.keywords

    # How freeg wifi can help you
    freegwifiHelpObj = HowFreegCanHelp.objects.all()
    freegwifiHelpObj = freegwifiHelpObj[0]
    context['category_divider_title1'] = freegwifiHelpObj.divider_title1
    context['category_divider_description1'] = freegwifiHelpObj.divider_description1
    context['category_divider_image1'] = freegwifiHelpObj.divider_image1.url
    context['category_divider_title2'] = freegwifiHelpObj.divider_title2
    context['category_divider_description2'] = freegwifiHelpObj.divider_description2
    context['category_divider_image2'] = freegwifiHelpObj.divider_image2.url
    context['category_divider_title3'] = freegwifiHelpObj.divider_title3
    context['category_divider_description3'] = freegwifiHelpObj.divider_description3
    context['category_divider_image3'] = freegwifiHelpObj.divider_image3.url

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata

    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # static blog images
    StaticBlogImagesobj = StaticBlogImages.objects.all()
    StaticBlogImagesobj = StaticBlogImagesobj[0]
    context['blog1image'] = StaticBlogImagesobj.blog1.url
    context['blog2image'] = StaticBlogImagesobj.blog2.url
    context['blog3image'] = StaticBlogImagesobj.blog3.url
    context['blog4image'] = StaticBlogImagesobj.blog4.url

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist
    #BestClientData
    bestclient = []
    allbestclient = BestClinetsImages.objects.all()
    allbestclient = allbestclient[:4]
    for singlebestclient in allbestclient:
        bestclient.append(singlebestclient.image.url)
    context['bestclient'] = bestclient

    # Case study data
    casestudy_model = ContactPageCaseStudy.objects.all()
    casestudy_model = casestudy_model[0]
    context['casestudy_image'] = casestudy_model.image.url
    context['casestudy_venue'] = casestudy_model.venue
    context['casestudy_description'] = casestudy_model.description

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # Allblogs data
    allBlogs = Blog.objects.all()
    bloglist = []
    counter = 0
    for singleBlog in allBlogs:
        if counter < 3:
            bloglist.append({
                'id': singleBlog.id,
                'title': singleBlog.title,
                'content': singleBlog.content,
                'image': singleBlog.image.url,
                'date': singleBlog.created_at
            })
            counter = counter + 1
    context['allblogs'] = bloglist
    #headquaters data
    headlist =[]
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname' : singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    #choicedata
    choicedata = []
    choicesall = ContactUs._meta.get_field('sector').choices
    for singlech in choicesall:
        choicedata.append(list(singlech)[0])
    context['choice'] = choicedata

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['instagram'] = freeginfo.instagram
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext


    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/contact2.html',context=context)

def formcareer(request,id):
    context = {}

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    CareerSelected = Careers.objects.get(id=id)
    ResponsibiltyAll = Responsibilty.objects.filter(career=CareerSelected)
    RequirementAll = Requirement.objects.filter(career=CareerSelected)
    PerksBenefitAll = PerksBenefit.objects.filter(career=CareerSelected)
    context['jid'] = CareerSelected.id
    context['jtitle'] = CareerSelected.position
    context['jlocation'] = CareerSelected.location
    context['jdescription'] = CareerSelected.description

    # title
    titleobj = WebsiteTitles.objects.all()
    titleobj = titleobj[0]
    career_form = titleobj.career_form
    context['pagetitle'] = career_form

    # MetaData
    MetaDataAllobj = MetaDataAll.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    singlemetadata = MetaDataAllobj.career_form
    context['metadata_author'] = singlemetadata.author
    context['metada_description'] = singlemetadata.description
    context['metadata_keywords'] = singlemetadata.keywords

    # How freeg wifi can help you
    freegwifiHelpObj = HowFreegCanHelp.objects.all()
    freegwifiHelpObj = freegwifiHelpObj[0]
    context['category_divider_title1'] = freegwifiHelpObj.divider_title1
    context['category_divider_description1'] = freegwifiHelpObj.divider_description1
    context['category_divider_image1'] = freegwifiHelpObj.divider_image1.url
    context['category_divider_title2'] = freegwifiHelpObj.divider_title2
    context['category_divider_description2'] = freegwifiHelpObj.divider_description2
    context['category_divider_image2'] = freegwifiHelpObj.divider_image2.url
    context['category_divider_title3'] = freegwifiHelpObj.divider_title3
    context['category_divider_description3'] = freegwifiHelpObj.divider_description3
    context['category_divider_image3'] = freegwifiHelpObj.divider_image3.url

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # static blog images
    StaticBlogImagesobj = StaticBlogImages.objects.all()
    StaticBlogImagesobj = StaticBlogImagesobj[0]
    context['blog1image'] = StaticBlogImagesobj.blog1.url
    context['blog2image'] = StaticBlogImagesobj.blog2.url
    context['blog3image'] = StaticBlogImagesobj.blog3.url
    context['blog4image'] = StaticBlogImagesobj.blog4.url

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist
    #BestClientData
    bestclient = []
    allbestclient = BestClinetsImages.objects.all()
    for singlebestclient in allbestclient:
        bestclient.append(singlebestclient.image.url)
    context['bestclient'] = bestclient

    # Case study data
    casestudy_model = ContactPageCaseStudy.objects.all()
    casestudy_model = casestudy_model[0]
    context['casestudy_image'] = casestudy_model.image.url
    context['casestudy_venue'] = casestudy_model.venue
    context['casestudy_description'] = casestudy_model.description

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # Allblogs data
    allBlogs = Blog.objects.all()
    bloglist = []
    counter = 0
    for singleBlog in allBlogs:
        if counter < 3:
            bloglist.append({
                'id': singleBlog.id,
                'title': singleBlog.title,
                'content': singleBlog.content,
                'image': singleBlog.image.url,
                'date': singleBlog.created_at
            })
            counter = counter + 1
    context['allblogs'] = bloglist
    #headquaters data
    headlist =[]
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname' : singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    #choicedata
    choicedata = []
    choicesall = ContactUs._meta.get_field('sector').choices
    for singlech in choicesall:
        choicedata.append(list(singlech)[0])
    context['choice'] = choicedata

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['instagram'] = freeginfo.instagram
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext



    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/formcareer.html',context=context)

# def courses(request,id):
#     context = {}
#
#     # Favicons images
#     Favicons = Favicon.objects.all()
#     Favicons = Favicons[0]
#
#     context['f_facebook'] = Favicons.facebook.url
#     context['f_instagram'] = Favicons.instagram.url
#     context['f_linkedin'] = Favicons.linkedin.url
#
#     context['f_nav_phone'] = Favicons.nav_phone.url
#     context['f_nav_email'] = Favicons.nav_email.url
#     context['f_footer_location'] = Favicons.footer_location.url
#
#     context['f_footer_email'] = Favicons.footer_email.url
#     context['f_footer_phone'] = Favicons.footer_phone.url
#     context['f_connect'] = Favicons.connect.url
#     context['f_base'] = Favicons.base.url
#     context['f_grow'] = Favicons.grow.url
#     context['f_arrow'] = Favicons.arrow.url
#
#
#     # bgimage
#     bgimageobj = BackGroundImage_NavigationBar.objects.all()
#     bgimageobj = bgimageobj[0]
#     fimage = bgimageobj.footer_image.url
#     context['footerimage'] = fimage
#
#     selectedcategory = freegcategory.objects.get(id = id)
#     # Website title
#     WebAll = WebsiteTitles_FreegCategory.objects.get(category=selectedcategory)
#     context['websitetitle'] = WebAll.title
#
#     #selectedcategorydata
#     context['category_name'] = selectedcategory.title
#     context['category_description'] = selectedcategory.description
#     context['category_image'] = selectedcategory.image.url
#     context['category_dashboardimage'] = selectedcategory.dashboardimage.url
#     context['dashboard_title1'] = selectedcategory.dashboard_title1
#     context['dashboard_title2'] = selectedcategory.dashboard_title2
#     context['dashboard_title3'] = selectedcategory.dashboard_title3
#     context['dashboard_description1'] = selectedcategory.dashboard_description1
#     context['dashboard_description2'] = selectedcategory.dashboard_description2
#     context['dashboard_description3'] = selectedcategory.dashboard_description3
#     context['bottombar'] = selectedcategory.bottombar
#     context['bottombarlink'] = selectedcategory.bottombarlink
#     context['category_divider_title1'] = selectedcategory.divider_title1
#     context['category_divider_description1'] = selectedcategory.divider_description1
#     context['category_divider_image1'] = selectedcategory.divider_image1.url
#     context['category_divider_title2'] = selectedcategory.divider_title2
#     context['category_divider_description2'] = selectedcategory.divider_description2
#     context['category_divider_image2'] = selectedcategory.divider_image2.url
#     context['category_divider_title3'] = selectedcategory.divider_title3
#     context['category_divider_description3'] = selectedcategory.divider_description3
#     context['category_divider_image3'] = selectedcategory.divider_image3.url
#     context['our_custom_dashboard_text'] = selectedcategory.our_custom_dashboard_text
#     context['read_more_visibility'] = selectedcategory.read_more_visibility
#
#
#     # title
#     context['pagetitle'] = selectedcategory.title
#
#     # MetaData
#
#     metadataobj_all = MetaDataFreeGCategory.objects.all()
#     for single_meta in metadataobj_all:
#         if single_meta.category.id == id :
#             context['metadata_author'] = single_meta.author
#             context['metada_description'] = single_meta.description
#             context['metadata_keywords'] = single_meta.keywords
#
#     # MetaDataAllobj = MetaDataAll.objects.all()
#     # MetaDataAllobj = MetaDataAllobj[0]
#     # singlemetadata = MetaDataAllobj.categories_showcase_of_our_our_diversity
#     # context['metadata_author'] = singlemetadata.author
#     # context['metada_description'] = singlemetadata.description
#     # context['metadata_keywords'] = singlemetadata.keywords
#
#     # branch office data
#     branchdata = []
#     BranchOfiicesObj = BranchOffices.objects.all()
#     for singlebranch in BranchOfiicesObj:
#         branchdata.append({
#             'city': singlebranch.cityname,
#             'contact': singlebranch.contact,
#             'email': singlebranch.email,
#         })
#     context['branchdata'] = branchdata
#     # channel partner data
#     channeldata = []
#     ChannelObj = ChannelPartners.objects.all()
#     for singlechannel in ChannelObj:
#         channeldata.append({
#             'city': singlechannel.cityname,
#             'contact': singlechannel.contact,
#             'email': singlechannel.email,
#         })
#     context['channeldata'] = channeldata
#
#     # headquaters data
#     headlist = []
#     headquaters = Freegheadquaters.objects.all()
#     for singlehead in headquaters:
#         headlist.append({
#             'cityname': singlehead.cityname,
#             'contact': singlehead.contact,
#             'email': singlehead.email,
#             'location': singlehead.location,
#             'longitude': singlehead.longitude,
#             'latitude': singlehead.latitude,
#             'cityname': singlehead.cityname,
#         })
#     context['headlist'] = headlist
#
#     # Freeg categories data
#     freegcategories = freegcategory.objects.all()
#     freegcategorieslist = []
#     for singlecategory in freegcategories:
#         freegcategorieslist.append({
#             'id': singlecategory.id,
#             'title': singlecategory.title,
#             'image': singlecategory.image.url
#         })
#     context['freegcategory'] = freegcategorieslist
#
#     # Pricing plan for category
#     pricingdata = []
#     tabledata  = []
#     pricingplanname = []
#     pricingplanprice = []
#     #Uncomment this line if different category have different plan
#     # plans_of_category = pricingplan.objects.filter(category=selectedcategory)
#     plans_of_category = pricingplan.objects.all()
#
#     #Uncomment this line if different category have different plan
#     # rows_of_category = pricingplanrow.objects.filter(category=selectedcategory)
#     rows_of_category = pricingplanrow.objects.all()
#
#     count = 0
#     for singleplan in plans_of_category:
#         singleplanlist = []
#         pricingplanname.append(singleplan.title)
#         pricingplanprice.append(singleplan.price)
#         for singlerow in rows_of_category:
#             if count == 0 :
#                 tabledata.append(singlerow.title)
#             if singleplan.category == singlerow.category:
#                 value = pricingplanvalue.objects.filter(plan=singleplan, row=singlerow)
#                 singleplanlist.append(value[0].value)
#         pricingdata.append(singleplanlist)
#         count = count + 1
#
#     context['pricingdata'] = pricingdata
#     context['tabledata'] = tabledata
#     context['pricingplanname'] = pricingplanname
#     context['pricingplanprice'] = pricingplanprice
#     planzipdata = zip(pricingdata, pricingplanname,pricingplanprice)
#     context['planzipdata'] = planzipdata
#
#     # testimonial data
#     testlist = []
#     testimonials = Testimonial.objects.filter(category=selectedcategory)
#     for singletest in testimonials:
#         testlist.append({
#             'name': singletest.name,
#             'description': singletest.description,
#             'image': singletest.image.url
#         })
#     context['testimonial'] = testlist
#
#     # freegwifi google facebook data
#     try:
#         freeginfo = FreegInfo.objects.all()
#         freeginfo = freeginfo[0]
#         context['facebook'] = freeginfo.facebook
#         context['twitter'] = freeginfo.twitter
#         context['linkedin'] = freeginfo.linkedin
#         context['googleplus'] = freeginfo.googleplus
#         context['emailid'] = freeginfo.saleemailid
#         context['semailid'] = freeginfo.supportemailid
#
#         context['instagram'] = freeginfo.instagram
#         context['freegcontact'] = freeginfo.contact
#
#         context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
#         context['freeglogo'] = freeginfo.logo.url
#         context['toplogo'] = freeginfo.toplogo.url
#         context['loginlink'] = freeginfo.loginlink
#
#         context['copyrighttext'] = freeginfo.copyrighttext
#         context['showcase_of_our_diversity_text'] = freeginfo.showcase_of_our_diversity_text
#
#
#     except Exception as e:
#         context['facebook'] = ""
#         context['twitter'] = ""
#         context['linkedin'] = ""
#         context['googleplus'] = ""
#         context['emailid'] = ""
#         context['freegcontact'] = ""
#         context['location'] = ""
#         context['aboutfreegwifi'] = ""
#     return render(request, 'app/courses.html',context=context)


def courses(request,name):
    context = {}

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    print 'manish '
    print name
    name = name.replace('_', ' ')
    selectedcategory = freegcategory.objects.get(title = name)
    id = selectedcategory.id

    # Website title
    WebAll = WebsiteTitles_FreegCategory.objects.get(category=selectedcategory)
    context['websitetitle'] = WebAll.title

    #selectedcategorydata
    context['category_name'] = selectedcategory.title
    context['category_description'] = selectedcategory.description
    context['category_image'] = selectedcategory.image.url
    context['category_dashboardimage'] = selectedcategory.dashboardimage.url
    context['dashboard_title1'] = selectedcategory.dashboard_title1
    context['dashboard_title2'] = selectedcategory.dashboard_title2
    context['dashboard_title3'] = selectedcategory.dashboard_title3
    context['dashboard_description1'] = selectedcategory.dashboard_description1
    context['dashboard_description2'] = selectedcategory.dashboard_description2
    context['dashboard_description3'] = selectedcategory.dashboard_description3
    context['bottombar'] = selectedcategory.bottombar
    context['bottombarlink'] = selectedcategory.bottombarlink
    context['category_divider_title1'] = selectedcategory.divider_title1
    context['category_divider_description1'] = selectedcategory.divider_description1
    context['category_divider_image1'] = selectedcategory.divider_image1.url
    context['category_divider_title2'] = selectedcategory.divider_title2
    context['category_divider_description2'] = selectedcategory.divider_description2
    context['category_divider_image2'] = selectedcategory.divider_image2.url
    context['category_divider_title3'] = selectedcategory.divider_title3
    context['category_divider_description3'] = selectedcategory.divider_description3
    context['category_divider_image3'] = selectedcategory.divider_image3.url
    context['our_custom_dashboard_text'] = selectedcategory.our_custom_dashboard_text
    context['read_more_visibility'] = selectedcategory.read_more_visibility


    # title
    context['pagetitle'] = selectedcategory.title

    # MetaData

    metadataobj_all = MetaDataFreeGCategory.objects.all()
    for single_meta in metadataobj_all:
        if single_meta.category.id == id :
            context['metadata_author'] = single_meta.author
            context['metada_description'] = single_meta.description
            context['metadata_keywords'] = single_meta.keywords

    # MetaDataAllobj = MetaDataAll.objects.all()
    # MetaDataAllobj = MetaDataAllobj[0]
    # singlemetadata = MetaDataAllobj.categories_showcase_of_our_our_diversity
    # context['metadata_author'] = singlemetadata.author
    # context['metada_description'] = singlemetadata.description
    # context['metadata_keywords'] = singlemetadata.keywords

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # Pricing plan for category
    pricingdata = []
    tabledata  = []
    pricingplanname = []
    pricingplanprice = []
    #Uncomment this line if different category have different plan
    # plans_of_category = pricingplan.objects.filter(category=selectedcategory)
    plans_of_category = pricingplan.objects.all()

    #Uncomment this line if different category have different plan
    # rows_of_category = pricingplanrow.objects.filter(category=selectedcategory)
    rows_of_category = pricingplanrow.objects.all()

    count = 0
    for singleplan in plans_of_category:
        singleplanlist = []
        pricingplanname.append(singleplan.title)
        pricingplanprice.append(singleplan.price)
        for singlerow in rows_of_category:
            if count == 0 :
                tabledata.append(singlerow.title)
            if singleplan.category == singlerow.category:
                value = pricingplanvalue.objects.filter(plan=singleplan, row=singlerow)
                singleplanlist.append(value[0].value)
        pricingdata.append(singleplanlist)
        count = count + 1

    context['pricingdata'] = pricingdata
    context['tabledata'] = tabledata
    context['pricingplanname'] = pricingplanname
    context['pricingplanprice'] = pricingplanprice
    planzipdata = zip(pricingdata, pricingplanname,pricingplanprice)
    context['planzipdata'] = planzipdata

    # testimonial data
    testlist = []
    testimonials = Testimonial.objects.filter(category=selectedcategory)
    for singletest in testimonials:
        testlist.append({
            'name': singletest.name,
            'description': singletest.description,
            'image': singletest.image.url
        })
    context['testimonial'] = testlist

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['instagram'] = freeginfo.instagram
        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink

        context['copyrighttext'] = freeginfo.copyrighttext
        context['showcase_of_our_diversity_text'] = freeginfo.showcase_of_our_diversity_text


    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/courses.html',context=context)

def pricing(request):
    context = {}
    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['instagram'] = freeginfo.instagram
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext


    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/pricing.html',context=context)

def team(request):
    context = {}

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    context['f_team_facebook'] = Favicons.team_facebook.url
    context['f_team_linkedin'] = Favicons.team_linkedin.url

    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    bgimage = bgimageobj.team_image.url
    context['bgimage'] = bgimage

    # title
    titleobj = WebsiteTitles.objects.all()
    titleobj = titleobj[0]
    team = titleobj.team
    context['pagetitle'] = team

    # MetaData
    MetaDataAllobj = MetaDataAll.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    singlemetadata = MetaDataAllobj.team
    context['metadata_author'] = singlemetadata.author
    context['metada_description'] = singlemetadata.description
    context['metadata_keywords'] = singlemetadata.keywords


    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # team data
    testlist = []
    testimonials = Team.objects.all()
    for singletest in testimonials:
        testlist.append({
            'name': singletest.name,
            'description': singletest.description,
            'image': singletest.image.url,
            'facebook': singletest.facebook ,
            'twitter': singletest.twitter,
            'linkedin': singletest.linkedin,
            'position': singletest.position
        })
    context['testimonial'] = testlist

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['instagram'] = freeginfo.instagram
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext

    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['contact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/team.html',context=context)

def morecategory(request):
    context = {}

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    # title
    titleobj = WebsiteTitles.objects.all()
    titleobj = titleobj[0]
    morecategory = titleobj.morecategory
    context['pagetitle'] = morecategory

    # MetaData
    MetaDataAllobj = MetaDataAll.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    singlemetadata = MetaDataAllobj.morecategory
    context['metadata_author'] = singlemetadata.author
    context['metada_description'] = singlemetadata.description
    context['metadata_keywords'] = singlemetadata.keywords

    #bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    bgimage = bgimageobj.more_category_image.url
    context['bgimage'] = bgimage


    #more categoirs
    morecatlist = []
    morecateobj = MoreCategories.objects.all()
    for singlecat in morecateobj:
        subcat = MoreCategorySubCategory.objects.filter(morecategory= singlecat)
        subdata = []
        for singlesubca in subcat:
            subdata.append({
                'id': singlesubca.id,
                'title': singlesubca.title,
                'image': singlesubca.image.url,
            })
        morecatlist.append({
            'title': singlecat.title,
            'id' : singlecat.id,
            'subdata' : subdata
        })
    context['morecat'] = morecatlist

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # team data
    testlist = []
    testimonials = Team.objects.all()
    for singletest in testimonials:
        testlist.append({
            'name': singletest.name,
            'description': singletest.description,
            'image': singletest.image.url,
            'facebook': singletest.facebook ,
            'twitter': singletest.twitter,
            'linkedin': singletest.linkedin,
            'position': singletest.position
        })
    context['testimonial'] = testlist

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['instagram'] = freeginfo.instagram
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext

    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['contact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/morecategory.html',context=context)

def blog(request):
    context = {}

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    # title
    titleobj = WebsiteTitles.objects.all()
    titleobj = titleobj[0]
    morecategory = titleobj.blogs
    context['pagetitle'] = morecategory

    # MetaData
    MetaDataAllobj = MetaDataAll.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    singlemetadata = MetaDataAllobj.blogs
    context['metadata_author'] = singlemetadata.author
    context['metada_description'] = singlemetadata.description
    context['metadata_keywords'] = singlemetadata.keywords

    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    bgimage = bgimageobj.blogs_image.url
    context['bgimage'] = bgimage


    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # static blog images
    StaticBlogImagesobj = StaticBlogImages.objects.all()
    StaticBlogImagesobj = StaticBlogImagesobj[0]
    context['blog1image'] = StaticBlogImagesobj.blog1.url
    context['blog2image'] = StaticBlogImagesobj.blog2.url
    context['blog3image'] = StaticBlogImagesobj.blog3.url
    context['blog4image'] = StaticBlogImagesobj.blog4.url

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # Allblogs data
    allBlogs = Blog.objects.all()
    bloglist =[]
    for singleBlog in allBlogs:
        bloglist.append({
            'id' : singleBlog.id,
        	'title' : singleBlog.title,
            'content' : singleBlog.content,
            'image' :singleBlog.image.url,
            'date' : singleBlog.created_at
        })
    context['allblogs'] = bloglist
    # context = {'allblogs' : bloglist}

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['instagram'] = freeginfo.instagram
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext

    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/blog.html',context=context)

def singleblog(request,id):
    context = {}

    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage


    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    blog = Blog.objects.get(id=id)

    context['title'] = blog.title
    context['content'] = blog.content
    context['para1'] = blog.para1
    context['para2'] = blog.para2
    context['para3'] = blog.para3
    context['para4'] = blog.para4
    context['para5'] = blog.para5
    context['image'] = blog.image.url
    try :
        context['image1'] = blog.image1.url
    except:
        context['image1'] = ''
    try :
        context['image2'] = blog.image2.url
    except:
        context['image2'] = ''
    try :
        context['image3'] = blog.image3.url
    except:
        context['image3'] = ''
    try :
        context['image4'] = blog.image4.url
    except:
        context['image4'] = ''
    try :
        context['image5'] = blog.image5.url
    except:
        context['image5'] = ''

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['instagram'] = freeginfo.instagram
        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext


    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""

    # Allblogs data
    allBlogs = Blog.objects.all()
    bloglist = []
    counter = 0
    for singleBlog in allBlogs:
        if counter < 3:
            bloglist.append({
                'id': singleBlog.id,
                'title': singleBlog.title,
                'content': singleBlog.content,
                'image': singleBlog.image.url,
                'date': singleBlog.created_at
            })
            counter = counter + 1
    context['allblogs'] = bloglist

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    return render(request, 'app/singleblog.html', context=context)

def singleblog1(request):
    context = {}

    # Knowmore link
    KnowMoreLinkobj = KnowMoreLink.objects.all()
    KnowMoreLinkobj = KnowMoreLinkobj[0]
    context['knowmore'] = KnowMoreLinkobj.title

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    # title
    # title
    titleobj = WebsiteTitles_Blogs.objects.all()
    titleobj = titleobj[0]
    blogs = titleobj.blog1
    context['pagetitle'] = blogs

    # MetaData
    MetaDataAllobj = MetaDataBlog.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    context['metadata_author'] = MetaDataAllobj.author1
    context['metada_description'] = MetaDataAllobj.description1
    context['metadata_keywords'] = MetaDataAllobj.keywords1

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # static blog images
    StaticBlogImagesobj = StaticBlogImages.objects.all()
    StaticBlogImagesobj = StaticBlogImagesobj[0]
    context['blog1image'] = StaticBlogImagesobj.blog1.url
    context['blog2image'] = StaticBlogImagesobj.blog2.url
    context['blog3image'] = StaticBlogImagesobj.blog3.url
    context['blog4image'] = StaticBlogImagesobj.blog4.url


    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['instagram'] = freeginfo.instagram
        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext


    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""

    # Allblogs data
    allBlogs = Blog.objects.all()
    bloglist = []
    counter = 0
    for singleBlog in allBlogs:
        if counter < 3:
            bloglist.append({
                'id': singleBlog.id,
                'title': singleBlog.title,
                'content': singleBlog.content,
                'image': singleBlog.image.url,
                'date': singleBlog.created_at
            })
            counter = counter + 1
    context['allblogs'] = bloglist
    return render(request, 'app/singleblog1.html', context=context)

def singleblog2(request):
    context = {}

    # Knowmore link
    KnowMoreLinkobj = KnowMoreLink.objects.all()
    KnowMoreLinkobj = KnowMoreLinkobj[0]
    context['knowmore'] = KnowMoreLinkobj.title

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    # title
    # title
    titleobj = WebsiteTitles_Blogs.objects.all()
    titleobj = titleobj[0]
    blogs = titleobj.blog2
    context['pagetitle'] = blogs

    # MetaData
    MetaDataAllobj = MetaDataBlog.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    context['metadata_author'] = MetaDataAllobj.author2
    context['metada_description'] = MetaDataAllobj.description2
    context['metadata_keywords'] = MetaDataAllobj.keywords2

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # static blog images
    StaticBlogImagesobj = StaticBlogImages.objects.all()
    StaticBlogImagesobj = StaticBlogImagesobj[0]
    context['blog1image'] = StaticBlogImagesobj.blog1.url
    context['blog2image'] = StaticBlogImagesobj.blog2.url
    context['blog3image'] = StaticBlogImagesobj.blog3.url
    context['blog4image'] = StaticBlogImagesobj.blog4.url

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['instagram'] = freeginfo.instagram
        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext


    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""

    # Allblogs data
    allBlogs = Blog.objects.all()
    bloglist = []
    counter = 0
    for singleBlog in allBlogs:
        if counter < 3:
            bloglist.append({
                'id': singleBlog.id,
                'title': singleBlog.title,
                'content': singleBlog.content,
                'image': singleBlog.image.url,
                'date': singleBlog.created_at
            })
            counter = counter + 1
    context['allblogs'] = bloglist
    return render(request, 'app/singleblog2.html', context=context)

def singleblog3(request):
    context = {}
    # Knowmore link
    KnowMoreLinkobj = KnowMoreLink.objects.all()
    KnowMoreLinkobj = KnowMoreLinkobj[0]
    context['knowmore'] = KnowMoreLinkobj.title

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage
    # title
    titleobj = WebsiteTitles_Blogs.objects.all()
    titleobj = titleobj[0]
    blogs = titleobj.blog3
    context['pagetitle'] = blogs

    # MetaData
    MetaDataAllobj = MetaDataBlog.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    context['metadata_author'] = MetaDataAllobj.author3
    context['metada_description'] = MetaDataAllobj.description3
    context['metadata_keywords'] = MetaDataAllobj.keywords3

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # static blog images
    StaticBlogImagesobj = StaticBlogImages.objects.all()
    StaticBlogImagesobj = StaticBlogImagesobj[0]
    context['blog1image'] = StaticBlogImagesobj.blog1.url
    context['blog2image'] = StaticBlogImagesobj.blog2.url
    context['blog3image'] = StaticBlogImagesobj.blog3.url
    context['blog4image'] = StaticBlogImagesobj.blog4.url


    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['instagram'] = freeginfo.instagram
        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext


    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""

    # Allblogs data
    allBlogs = Blog.objects.all()
    bloglist = []
    counter = 0
    for singleBlog in allBlogs:
        if counter < 3:
            bloglist.append({
                'id': singleBlog.id,
                'title': singleBlog.title,
                'content': singleBlog.content,
                'image': singleBlog.image.url,
                'date': singleBlog.created_at
            })
            counter = counter + 1
    context['allblogs'] = bloglist
    return render(request, 'app/singleblog3.html', context=context)

def casestudy(request):
    context = {}

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    CaseStudyVisibilityobj = CaseStudyVisibility.objects.all()
    CaseStudyVisibilityobj = CaseStudyVisibilityobj[0]
    context['casestudy_visible'] = CaseStudyVisibilityobj.casestudy_visible

    # title
    titleobj = WebsiteTitles.objects.all()
    titleobj = titleobj[0]
    casestudy = titleobj.casestudy
    context['pagetitle'] = casestudy
    # MetaData
    MetaDataAllobj = MetaDataAll.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    singlemetadata = MetaDataAllobj.casestudy
    context['metadata_author'] = singlemetadata.author
    context['metada_description'] = singlemetadata.description
    context['metadata_keywords'] = singlemetadata.keywords

    #bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    bgimage = bgimageobj.casestudy_image.url
    context['bgimage'] = bgimage


    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata


    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist
    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist
    # Allcasestudy data
    allCasestudy = Casestudy.objects.all()
    casestudylist =[]
    for singleCase in allCasestudy:
        casestudylist.append({
            'id' : singleCase.id,
        	'title' : singleCase.title,
            'content' : singleCase.content,
            'image' :singleCase.image.url,
            'date' : singleCase.created_at,
        })
    context['allcase'] = casestudylist

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['instagram'] = freeginfo.instagram
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext

    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/casestudy.html',context=context)

def singleblog4(request):
    context = {}
    # Knowmore link
    KnowMoreLinkobj = KnowMoreLink.objects.all()
    KnowMoreLinkobj = KnowMoreLinkobj[0]
    context['knowmore'] = KnowMoreLinkobj.title

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    # title
    titleobj = WebsiteTitles_Blogs.objects.all()
    titleobj = titleobj[0]
    blogs = titleobj.blog4
    context['pagetitle'] = blogs

    # MetaData
    MetaDataAllobj = MetaDataBlog.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    context['metadata_author'] = MetaDataAllobj.author4
    context['metada_description'] = MetaDataAllobj.description4
    context['metadata_keywords'] = MetaDataAllobj.keywords4

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # static blog images
    StaticBlogImagesobj = StaticBlogImages.objects.all()
    StaticBlogImagesobj = StaticBlogImagesobj[0]
    context['blog1image'] = StaticBlogImagesobj.blog1.url
    context['blog2image'] = StaticBlogImagesobj.blog2.url
    context['blog3image'] = StaticBlogImagesobj.blog3.url
    context['blog4image'] = StaticBlogImagesobj.blog4.url

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['instagram'] = freeginfo.instagram
        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext


    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""

    # Allblogs data
    allBlogs = Blog.objects.all()
    bloglist = []
    counter = 0
    for singleBlog in allBlogs:
        if counter < 3:
            bloglist.append({
                'id': singleBlog.id,
                'title': singleBlog.title,
                'content': singleBlog.content,
                'image': singleBlog.image.url,
                'date': singleBlog.created_at
            })
            counter = counter + 1
    context['allblogs'] = bloglist
    return render(request, 'app/singleblog4.html', context=context)

def singlecasestudy(request,id):
    context = {}

    #Knowmore link
    KnowMoreLinkobj = KnowMoreLink.objects.all()
    KnowMoreLinkobj = KnowMoreLinkobj[0]
    context['knowmore'] = KnowMoreLinkobj.title

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    # MetaData

    metadataobj_all = MetaDataCaseStudy.objects.all()
    for single_meta in metadataobj_all:
        if single_meta.casestudy.id == id:
            context['metadata_author'] = single_meta.author
            context['metada_description'] = single_meta.description
            context['metadata_keywords'] = single_meta.keywords


    # MetaDataAllobj = MetaDataAll.objects.all()
    # MetaDataAllobj = MetaDataAllobj[0]
    # singlemetadata = MetaDataAllobj.casestudy
    # context['metadata_author'] = singlemetadata.author
    # context['metada_description'] = singlemetadata.description
    # context['metadata_keywords'] = singlemetadata.keywords

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    casestudy = Casestudy.objects.get(id=id)

    context['title'] = casestudy.title
    context['content'] = casestudy.content
    context['headerimage'] = casestudy.image.url
    paras = []
    paraobj = CaseStudyParagraph.objects.filter(casestudy=casestudy)
    paralist = []
    for singlepara in paraobj:
        paralist.append({
            'paragraph':singlepara.paragraph,
            'margintop': singlepara.margintop,
            'marginbottom': singlepara.marginbottom,
            'ischeckpoint': singlepara.ischeckpoint
        })
    context['para'] = paralist

    # title
    context['pagetitle'] = casestudy.title


    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['instagram'] = freeginfo.instagram
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext


    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""

    # Allcasestudy data
    allCasestudy = Casestudy.objects.all()
    casestudylist = []
    counter = 0
    for singleCase in allCasestudy:
        if int(singleCase.id) != int(id) and counter < 3 :
            casestudylist.append({
                'id': singleCase.id,
                'title': singleCase.title,
                'content': singleCase.content,
                'image': singleCase.image.url,
                'date': singleCase.created_at
            })
            counter += 1
    context['allcase'] = casestudylist
    return render(request, 'app/singlecasestudy.html', context=context)

def aboutus(request):
    context = {}

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    # title
    titleobj = WebsiteTitles.objects.all()
    titleobj = titleobj[0]
    aboutus = titleobj.aboutus
    context['pagetitle'] = aboutus

    # MetaData
    MetaDataAllobj = MetaDataAll.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    singlemetadata = MetaDataAllobj.aboutus
    context['metadata_author'] = singlemetadata.author
    context['metada_description'] = singlemetadata.description
    context['metadata_keywords'] = singlemetadata.keywords


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    bgimage = bgimageobj.about_us_image.url
    context['bgimage'] = bgimage


    started = []
    vision = []
    whatwedo = []

    startedobj = AboutUs_How_We_Started.objects.all()
    for single in startedobj:
        started.append(single.content)
    context['started'] = started

    visionobj = AboutUs_Our_Vision.objects.all()
    for single in visionobj:
        vision.append(single)
    context['vision'] = vision

    whatwedoobj = AboutUs_What_We_Do.objects.all()
    for single in whatwedoobj:
        whatwedo.append({
            'image' : single.image.url,
            'content' : single.content,
            'title' : single.title
        })
    context['whatwedo'] = whatwedo
    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist
    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist


    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['instagram'] = freeginfo.instagram
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext

    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/aboutus.html',context=context)

def career(request):
    context = {}

    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage
    # title
    titleobj = WebsiteTitles.objects.all()
    titleobj = titleobj[0]
    career = titleobj.career
    context['pagetitle'] = career

    # MetaData
    MetaDataAllobj = MetaDataAll.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    singlemetadata = MetaDataAllobj.career
    context['metadata_author'] = singlemetadata.author
    context['metada_description'] = singlemetadata.description
    context['metadata_keywords'] = singlemetadata.keywords


    CareerSubheadingobj = CareerSubheading.objects.all()
    CareerSubheadingobj = CareerSubheadingobj[0]
    context['careersubheading'] = CareerSubheadingobj.subheading

    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    bgimage = bgimageobj.careers_image.url
    context['bgimage'] = bgimage


    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    #careers data

    careeerdata = []
    allcareers = Careers.objects.all()
    for singlecareer in allcareers:
        careeerdata.append({
            'id' : singlecareer.id,
            'position' : singlecareer.position,
            'location' : singlecareer.location
        })
    context['career'] = careeerdata
    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['instagram'] = freeginfo.instagram
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext

    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/career.html',context=context)

def careerdetail(request,id):
    context = {}
    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    # title
    titleobj = WebsiteTitles.objects.all()
    titleobj = titleobj[0]
    careerdetail = titleobj.careerdetail
    context['pagetitle'] = careerdetail

    # MetaData
    MetaDataAllobj = MetaDataAll.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    singlemetadata = MetaDataAllobj.careerdetail
    context['metadata_author'] = singlemetadata.author
    context['metada_description'] = singlemetadata.description
    context['metadata_keywords'] = singlemetadata.keywords

    CareerSelected = Careers.objects.get(id = id)
    ResponsibiltyAll = Responsibilty.objects.filter(career=CareerSelected)
    RequirementAll = Requirement.objects.filter(career=CareerSelected)
    PerksBenefitAll = PerksBenefit.objects.filter(career=CareerSelected)
    context['jid'] = CareerSelected.id
    context['jtitle'] = CareerSelected.position
    context['jlocation'] = CareerSelected.location
    context['jdescription'] = CareerSelected.description

    ResponsibiltyData = []
    for sResponsibiltyAll in ResponsibiltyAll:
        ResponsibiltyData.append(sResponsibiltyAll.title)
    context['responsiblity'] = ResponsibiltyData

    RequirementData = []
    for sRequirementAll in RequirementAll:
        RequirementData.append(sRequirementAll.title)
    context['requirement'] = RequirementData

    PerksBenefitData = []
    for sPerksBenefitAll in PerksBenefitAll:
        PerksBenefitData.append(sPerksBenefitAll.title)
    context['perksbenefit'] = PerksBenefitData

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['instagram'] = freeginfo.instagram
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext

    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/careerdetail.html',context=context)

def formsuccess(request):
    context = {}
    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage

    # title
    titleobj = WebsiteTitles.objects.all()
    titleobj = titleobj[0]
    contact_form_after_completion = titleobj.contact_form_after_completion
    context['pagetitle'] = contact_form_after_completion

    # MetaData
    MetaDataAllobj = MetaDataAll.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    singlemetadata = MetaDataAllobj.contact_form_after_completion
    context['metadata_author'] = singlemetadata.author
    context['metada_description'] = singlemetadata.description
    context['metadata_keywords'] = singlemetadata.keywords

    # steps to install wifi data
    stepslist = []
    Stepshomepagelist = Contact_Form_Success_Steps.objects.all()
    for singlestep in Stepshomepagelist:
        stepslist.append({
            'sequence': singlestep.sequence,
            'title': singlestep.title
        })
    context['steplist'] = stepslist

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    #careers data

    careeerdata = []
    allcareers = Careers.objects.all()
    for singlecareer in allcareers:
        careeerdata.append({
            'position' : singlecareer.position,
            'location' : singlecareer.location
        })
    context['career'] = careeerdata

    # Case study data
    casestudy_model = ContactPageCaseStudy.objects.all()
    casestudy_model = casestudy_model[0]
    context['casestudy_image'] = casestudy_model.image.url
    context['casestudy_venue'] = casestudy_model.venue
    context['casestudy_description'] = casestudy_model.description

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['instagram'] = freeginfo.instagram
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact

        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext

    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/formsuccess.html',context=context)

def careerfinal(request):
    context = {}
    # Favicons images
    Favicons = Favicon.objects.all()
    Favicons = Favicons[0]

    context['f_facebook'] = Favicons.facebook.url
    context['f_instagram'] = Favicons.instagram.url
    context['f_linkedin'] = Favicons.linkedin.url

    context['f_nav_phone'] = Favicons.nav_phone.url
    context['f_nav_email'] = Favicons.nav_email.url
    context['f_footer_location'] = Favicons.footer_location.url

    context['f_footer_email'] = Favicons.footer_email.url
    context['f_footer_phone'] = Favicons.footer_phone.url
    context['f_connect'] = Favicons.connect.url
    context['f_base'] = Favicons.base.url
    context['f_grow'] = Favicons.grow.url
    context['f_arrow'] = Favicons.arrow.url


    # bgimage
    bgimageobj = BackGroundImage_NavigationBar.objects.all()
    bgimageobj = bgimageobj[0]
    fimage = bgimageobj.footer_image.url
    context['footerimage'] = fimage
    context['footerimage'] = fimage

    # title
    titleobj = WebsiteTitles.objects.all()
    titleobj = titleobj[0]
    career_form_after_completion = titleobj.career_form_after_completion
    context['pagetitle'] = career_form_after_completion

    # MetaData
    MetaDataAllobj = MetaDataAll.objects.all()
    MetaDataAllobj = MetaDataAllobj[0]
    singlemetadata = MetaDataAllobj.career_form_after_completion
    context['metadata_author'] = singlemetadata.author
    context['metada_description'] = singlemetadata.description
    context['metadata_keywords'] = singlemetadata.keywords

    # static blog images
    StaticBlogImagesobj = StaticBlogImages.objects.all()
    StaticBlogImagesobj = StaticBlogImagesobj[0]
    context['blog1image'] = StaticBlogImagesobj.blog1.url
    context['blog2image'] = StaticBlogImagesobj.blog2.url
    context['blog3image'] = StaticBlogImagesobj.blog3.url
    context['blog4image'] = StaticBlogImagesobj.blog4.url

    # branch office data
    branchdata = []
    BranchOfiicesObj = BranchOffices.objects.all()
    for singlebranch in BranchOfiicesObj:
        branchdata.append({
            'city': singlebranch.cityname,
            'contact': singlebranch.contact,
            'email': singlebranch.email,
        })
    context['branchdata'] = branchdata
    # channel partner data
    channeldata = []
    ChannelObj = ChannelPartners.objects.all()
    for singlechannel in ChannelObj:
        channeldata.append({
            'city': singlechannel.cityname,
            'contact': singlechannel.contact,
            'email': singlechannel.email,
        })
    context['channeldata'] = channeldata

    # Freeg categories data
    freegcategories = freegcategory.objects.all()
    freegcategorieslist = []
    for singlecategory in freegcategories:
        freegcategorieslist.append({
            'id': singlecategory.id,
            'title': singlecategory.title,
            'image': singlecategory.image.url
        })
    context['freegcategory'] = freegcategorieslist

    #careers data

    careeerdata = []
    allcareers = Careers.objects.all()
    for singlecareer in allcareers:
        careeerdata.append({
            'position' : singlecareer.position,
            'location' : singlecareer.location
        })
    context['career'] = careeerdata

    # Case study data
    casestudy_model = ContactPageCaseStudy.objects.all()
    casestudy_model = casestudy_model[0]
    context['casestudy_image'] = casestudy_model.image.url
    context['casestudy_venue'] = casestudy_model.venue
    context['casestudy_description'] = casestudy_model.description

    # headquaters data
    headlist = []
    headquaters = Freegheadquaters.objects.all()
    for singlehead in headquaters:
        headlist.append({
            'cityname': singlehead.cityname,
            'contact': singlehead.contact,
            'email': singlehead.email,
            'location': singlehead.location,
            'longitude': singlehead.longitude,
            'latitude': singlehead.latitude,
            'cityname': singlehead.cityname,
        })
    context['headlist'] = headlist

    # freegwifi google facebook data
    try:
        freeginfo = FreegInfo.objects.all()
        freeginfo = freeginfo[0]
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['instagram'] = freeginfo.instagram
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact
        
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink
        context['copyrighttext'] = freeginfo.copyrighttext

    except Exception as e:
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    return render(request, 'app/careerfinal.html',context=context)
