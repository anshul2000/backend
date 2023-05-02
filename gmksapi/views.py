import base64
from rest_framework.decorators import action
from rest_framework.renderers import BaseRenderer
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, Http404
from .forms import *
from .models import *
from django.conf import settings
import math
import random

from rest_framework.parsers import JSONParser
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from drf_pdf.response import PDFFileResponse
from drf_pdf.renderer import PDFRenderer
from django.contrib.sites.shortcuts import get_current_site
import os
from rest_framework.decorators import api_view
from django.http import FileResponse
from wsgiref.util import FileWrapper
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import datetime
# Create your views here.


@api_view(('POST',))
def home(request):
    if request.method == 'POST':
        print(request.POST['loc'], request.POST['category'], request.POST['language'])
        category=str(request.POST['category'])
        language = str(request.POST['language'])
        try:
            data=Data.objects.get(loc=request.POST['loc'],category=category.lower(), language=language.lower())
            print("Will be updated")
        except:
            data = Data.objects.create(loc=request.POST['loc'],category=category.lower(), language=language.lower())
            print("Will be Created")
        
        form = DataForm(request.POST, request.FILES, instance=data)
        if (request.POST['loc']==''):
            # print("loc is dead")
            form.data['loc']='General'
        # print(form)
        if form.is_valid():
            # file is saved
            msg = "Data Posted Successfully"
            print(msg)
            
            if (form.data['loc']==''):
                form.data['loc']='General'

            

            print(form.data['loc'], form.data['language'])
            form.save()
            print(form.data['loc'],form.data['category'])
            # datas = Data.objects.get(loc=form.data['loc'],category=form.data['category'])
            # print(datas)
            # print(datas['upload'])
            return Response({'status': status.HTTP_200_OK, "msg" :msg})
        
        else:
            print(form.errors)

            form = DataForm()
            context = {
                'errors': form.errors,
                'form': form,
            }
            return Response({'errors': form.errors,
                'form': form,})
    else:
        form = DataForm()

        context = {
            'form': form,
        }
        return Response({'status': status.HTTP_200_OK})


def data_list(request):
    if request.method == 'GET':
        datas = Data.objects.all()
        serializer = DataSerializer(datas, many=True)
        return JsonResponse(serializer.data, safe=False)


def data(request, pk):
    if request.method == 'GET':
        print(pk)
        datas = Data.objects.get(loc=pk)
        print(datas)
        serializer = DataSerializer(datas)
        print(str(get_current_site(request))+serializer.data['upload'])
        string = serializer.data['upload'].split('/')
        filepath = os.path.join('media', string[2])
        with open(filepath, 'rb') as report:
            response = HttpResponse(FileWrapper(
                report), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="%s"' % string[2]
            return response


class BinaryFileRenderer(BaseRenderer):
    media_type = 'application/octet-stream'
    format = None
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data

def pre(loc):
    r=loc.split(" ")
    if len(r)>1:
        return(str(r[0].capitalize()+" "+r[-1].capitalize()))
    return(str(r[0].capitalize()))

@api_view(('GET',))
@action(detail=True, methods=['get'], renderer_classes=(BinaryFileRenderer,))
def download( request, pk,location,lang, *args, **kwargs ):
    location=pre(location)
    print(location)
    print('*'*100)
    datas = Data.objects.get(loc=location,category=str(pk).lower(),language=str(lang).lower())
    print('*'*100)
    serializer = DataSerializer(datas)
    print(serializer.data['upload'])
    string = serializer.data['upload'].split('/')
    filepath = os.path.join('media', string[2])
    print(filepath)
    with open(filepath, 'rb') as report:
        print('success')
        report_encoded = base64.b64encode(report.read())
        return Response({'status': status.HTTP_200_OK, 'report': report_encoded})


@csrf_exempt
@api_view(('POST','GET','PUT'))
def number(request):
    if request.method == 'PUT':
        DATA=JSONParser().parse(request)

        a=UserContact.objects.create()
        serializer=ContactSerializer(a,data=DATA)
        print(serializer)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            print('sucess')
            return JsonResponse(serializer.data)
        print(serializer.errors)
        a.delete()
        return JsonResponse(serializer.errors,status=400)

        # obj=UserContact.objects.create(number=int(request.POST['number']))
        # obj.save()
        # return Response({'status': status.HTTP_200_OK})
    elif request.method=='GET' :
        contacts = UserContact.objects.all()
        serializer = ContactSerializer(contacts, many =True)
        return Response({'status': status.HTTP_200_OK, 'data': serializer.data})
        
from twilio.rest import Client
@csrf_exempt
@api_view(('POST','GET','PUT'))
def sms(request):
    res=""
    if request.method == 'GET':
        contact=UserContact.objects.all()
        client = Client('AC2a94d3d3b15c0cfaf5a5431f0e2323b0', '1adbbd64bde6f14356a610c21059af67')
        for c in contact:
            if c.number:
                try:
                    message = client.messages \
                        .create(
                            body='New document uploaded on "Anumaan" website, please check.    অনুমান" ওয়েবসাইটে নতুন ডকুমেন্ট আপলোড করা হয়েছে, অনুগ্রহ করে চেক করুন।',
                            from_='+19206587995',
                            to="+91"+str(c.number)
                        )
                    
                    print(message.sid)
                except:
                    res+="+91"+str(c.number) +" is unverified at Twillo. \n"
    
    return Response({'status': status.HTTP_200_OK,  'response': res})


@csrf_exempt
@api_view(('POST','PUT'))
def text(request):
    res=""
    # print("*"*100)
    # DATA=JSONParser().parse(request)
    # print(DATA)
    # print("*"*100)
    if request.method == 'POST':
        form = TextForm(request.POST, request.FILES)
        text=form.data['text']
        print(text)
        contact=UserContact.objects.all()
        client = Client('AC2a94d3d3b15c0cfaf5a5431f0e2323b0', '1adbbd64bde6f14356a610c21059af67')
        for c in contact:
            if c.number:
                try:
                    message = client.messages \
                        .create(
                            body=str(text),
                            from_='+19206587995',
                            to="+91"+str(c.number)
                        )
                    
                    print(message.sid)
                except:
                    res+="+91"+str(c.number) +" is unverified at Twillo. \n"
    
    return Response({'status': status.HTTP_200_OK,  'response': res})


@csrf_exempt
@api_view(('GET','PUT'))
def number2(request):
    res=""
    if request.method == 'PUT':
        DATA=JSONParser().parse(request)
        client = Client('AC2a94d3d3b15c0cfaf5a5431f0e2323b0', '1adbbd64bde6f14356a610c21059af67')
        number=DATA['number']
        try:
            message = client.messages \
                .create(
                    body='YOur App link is : Lorem Ipsum',
                    from_='+19206587995',
                    to="+91"+str(number)
                )
            print(message.sid)
        except:
            res+="+91"+str(number) +" is unverified at Twillo. \n"        
        
        return Response({'status': status.HTTP_200_OK,  'response': res})

    elif request.method=='GET' :
        contacts = UserContact.objects.all()
        serializer = ContactSerializer(contacts, many =True)
        return Response({'status': status.HTTP_200_OK, 'data': serializer.data})
    
from datetime import datetime,timedelta
from datetime import date

# import time
import time
@csrf_exempt
@api_view(('GET','PUT',"POST"))
def awareness(request):
    if request.method == 'POST' or request.method == 'PUT' :
        form = AwarenessForm(request.POST, request.FILES)

        if form.is_valid():
            msg = "Data Posted Successfully"
            print("*"*100)
            print(msg)
            form.save()
            return Response({'status': status.HTTP_200_OK})
    
        else:
            print(form.errors)

            form = AwarenessForm()
            context = {
                'errors': form.errors,
                'form': form,
            }
            return Response({'errors': form.errors,
                'form': form})
    elif request.method =="GET":
        print(date.today())
        t= time.localtime()
        current_time=time.strftime("%H:%M:%S",t)
        print(current_time)
        date_threshold = date.today() - timedelta(days=10000)
        contacts = Awareness.objects.values('id','loc','date','event','time').filter(date__gte=date_threshold).order_by('-date')
        serializer=AwarenessSerializer(contacts,many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)
       
@api_view(('GET',))
@action(detail=True, methods=['get'], renderer_classes=(BinaryFileRenderer,))
def awareness_download( request, id, *args, **kwargs ):
    print("awareness_download", id)
    print('*'*100)
    datas = Awareness.objects.get(id=id)
    serializer = AwarenessSerializer(datas)
    print(serializer.data['file'])
    string = serializer.data['file'].split('/')
    filepath = os.path.join('media', string[2])
    print(filepath)
    with open(filepath, 'rb') as report:
        print('success')
        report_encoded = base64.b64encode(report.read())
        return Response({'status': status.HTTP_200_OK, 'file': report_encoded})
    
@api_view(('GET',))
@action(detail=True, methods=['get'], renderer_classes=(BinaryFileRenderer,))
def event_download(request, *args, **kwargs):
    # location=pre(location)
    # print(location)
    datas = Data.objects.get(loc="general",category="event")
    serializer = DataSerializer(datas)
    string = serializer.data['upload'].split('/')
    filepath = os.path.join('media', string[2])
    with open(filepath, 'rb') as report:
        report_encoded = base64.b64encode(report.read())
        return Response({'status': status.HTTP_200_OK, 'report': report_encoded})

