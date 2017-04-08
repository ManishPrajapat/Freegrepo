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


def homepage(request):
    context = {}

    #backgroudn image larger than life
    bgobj = Largebackgroundimage.objects.all()
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
    print  branchdata

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
            'image' : singlecategory.image.url
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

    #steps to install wifi data
    stepslist = []
    Stepshomepagelist = Stepshomepage.objects.all()
    for singlestep in Stepshomepagelist:
        stepslist.append({
            'sequence' : singlestep.sequence,
            'title' : singlestep.title
        })
    context['steplist'] = stepslist

    #freegwifi google facebook data
    try :
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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink

    except Exception as e:
        print 'what the heck'
        context['facebook'] = ""
        context['twitter'] = ""
        context['linkedin'] = ""
        context['googleplus'] = ""
        context['emailid'] = ""
        context['freegcontact'] = ""
        context['location'] = ""
        context['aboutfreegwifi'] = ""
    print context['freegcontact']
    return render(request, 'app/index.html',context=context)

@csrf_exempt
def cformsubmit(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        position = request.POST['position']
        resume = request.FILES['resume']
        print resume
        cf = CareerForm(name=name,email=email,contact=contact,position=position,resume=resume)
        cf.save()
        return HttpResponseRedirect('/web/careerfinal/')

@csrf_exempt
def contactus(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        sector = request.POST['sector']
        businessname = request.POST['businessname']
        address = request.POST['address']
        officeno = request.POST['officeno']
        comments = request.POST['comments']
        contact_obj = ContactUs(name=name,email=email, contact=contact,comments=comments,
                                businessname=businessname, sector=sector, address=address, officeno=officeno)
        contact_obj.save()
        return HttpResponseRedirect('/web/formsuccess')

def contact(request):
    context = {}

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
    # backgroudn image larger than life
    bgobj = Largebackgroundimage.objects.all()
    bgobj = bgobj[0]
    context['mainbackground'] = bgobj.contact.url
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
        locationlist = freeginfo.location.splitlines()
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink


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

def formcareer(request,id):
    context = {}

    CareerSelected = Careers.objects.get(id=id)
    ResponsibiltyAll = Responsibilty.objects.filter(career=CareerSelected)
    RequirementAll = Requirement.objects.filter(career=CareerSelected)
    PerksBenefitAll = PerksBenefit.objects.filter(career=CareerSelected)
    context['jid'] = CareerSelected.id
    context['jtitle'] = CareerSelected.position
    context['jlocation'] = CareerSelected.location
    context['jdescription'] = CareerSelected.description

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
    # backgroudn image larger than life
    bgobj = Largebackgroundimage.objects.all()
    bgobj = bgobj[0]
    context['mainbackground'] = bgobj.contact.url
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
        locationlist = freeginfo.location.splitlines()
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink


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


def courses(request,id):
    context = {}

    selectedcategory = freegcategory.objects.get(id = id)

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

    context['category_divider_title1'] = selectedcategory.divider_title1
    context['category_divider_description1'] = selectedcategory.divider_description1
    context['category_divider_image1'] = selectedcategory.divider_image1.url
    context['category_divider_title2'] = selectedcategory.divider_title2
    context['category_divider_description2'] = selectedcategory.divider_description2
    context['category_divider_image2'] = selectedcategory.divider_image2.url
    context['category_divider_title3'] = selectedcategory.divider_title3
    context['category_divider_description3'] = selectedcategory.divider_description3
    context['category_divider_image3'] = selectedcategory.divider_image3.url

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
    print pricingdata
    print tabledata
    print pricingplanname
    print pricingplanprice

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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink


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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink


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
    # backgroudn image larger than life
    bgobj = Largebackgroundimage.objects.all()
    bgobj = bgobj[0]
    context['mainbackground'] = bgobj.ourteam.url
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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink

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



def blog(request):
    context = {}
    # backgroudn image larger than life
    bgobj = Largebackgroundimage.objects.all()
    bgobj = bgobj[0]
    context['mainbackground'] = bgobj.blog.url
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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink

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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink


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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink


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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink


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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink


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
    # backgroudn image larger than life
    bgobj = Largebackgroundimage.objects.all()
    bgobj = bgobj[0]
    context['mainbackground'] = bgobj.casestudy.url

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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink

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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink


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
    context['para1'] = casestudy.para1
    context['para2'] = casestudy.para2
    context['para3'] = casestudy.para3
    context['para4'] = casestudy.para4
    context['para5'] = casestudy.para5
    context['image'] = casestudy.image.url
    try :
        context['image1'] = casestudy.image1.url
    except:
        context['image1'] = ''
    try :
        context['image2'] = casestudy.image2.url
    except:
        context['image2'] = ''
    try :
        context['image3'] = casestudy.image3.url
    except:
        context['image3'] = ''
    try :
        context['image4'] = casestudy.image4.url
    except:
        context['image4'] = ''
    try :
        context['image5'] = casestudy.image5.url
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
        context['instagram'] = freeginfo.instagram
        context['facebook'] = freeginfo.facebook
        context['twitter'] = freeginfo.twitter
        context['linkedin'] = freeginfo.linkedin
        context['googleplus'] = freeginfo.googleplus
        context['emailid'] = freeginfo.saleemailid
        context['semailid'] = freeginfo.supportemailid

        context['freegcontact'] = freeginfo.contact
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink


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
    for singleCase in allCasestudy:
        if int(singleCase.id) != int(id) :
            print singleCase.id
            print  id
            casestudylist.append({
                'id': singleCase.id,
                'title': singleCase.title,
                'content': singleCase.content,
                'image': singleCase.image.url,
                'date': singleCase.created_at,
            })
    context['allcase'] = casestudylist
    return render(request, 'app/singlecasestudy.html', context=context)



def aboutus(request):
    context = {}

    # backgroudn image larger than life
    bgobj = Largebackgroundimage.objects.all()
    bgobj = bgobj[0]
    context['mainbackground'] = bgobj.casestudy.url
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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink

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

    # backgroudn image larger than life
    bgobj = Largebackgroundimage.objects.all()
    bgobj = bgobj[0]
    context['mainbackground'] = bgobj.casestudy.url

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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink

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


    # backgroudn image larger than life
    bgobj = Largebackgroundimage.objects.all()
    bgobj = bgobj[0]
    context['mainbackground'] = bgobj.casestudy.url

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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink

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

    # backgroudn image larger than life
    bgobj = Largebackgroundimage.objects.all()
    bgobj = bgobj[0]
    context['mainbackground'] = bgobj.casestudy.url

    # steps to install wifi data
    stepslist = []
    Stepshomepagelist = Stepshomepage.objects.all()
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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink

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

    # backgroudn image larger than life
    bgobj = Largebackgroundimage.objects.all()
    bgobj = bgobj[0]
    context['mainbackground'] = bgobj.casestudy.url
    # static blog images
    StaticBlogImagesobj = StaticBlogImages.objects.all()
    StaticBlogImagesobj = StaticBlogImagesobj[0]
    context['blog1image'] = StaticBlogImagesobj.blog1.url
    context['blog2image'] = StaticBlogImagesobj.blog2.url
    context['blog3image'] = StaticBlogImagesobj.blog3.url
    context['blog4image'] = StaticBlogImagesobj.blog4.url


    # steps to install wifi data
    stepslist = []
    Stepshomepagelist = Stepshomepage.objects.all()
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
        locationlist = freeginfo.location.split('\n')
        context['location'] = locationlist
        context['longitude'] = freeginfo.longitude
        context['latitude'] = freeginfo.latitude
        context['aboutfreegwifi'] = freeginfo.aboutfreegwifi
        context['freeglogo'] = freeginfo.logo.url
        context['toplogo'] = freeginfo.toplogo.url
        context['loginlink'] = freeginfo.loginlink

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
