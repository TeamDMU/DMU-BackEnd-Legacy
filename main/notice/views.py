from dataclasses import fields
from logging import exception
from multiprocessing.sharedctypes import Value
from re import A, L
from django.http import HttpResponse,JsonResponse,Http404
from django.views import View
from .models import Noti , Schedule , Menu
from django.core import serializers
from http import HTTPStatus
import json
import re
# Create your views here.


class NoticeList(View):
    def get(self,request,major):
        try:
            notice = Noti.objects.using('crawled_data').filter(major_code = major).order_by('-num')
            data = serializers.serialize("json", list(
                notice), fields=('num', 'title','date', 'writer'))
            temp = json.loads(data)     
            datalist = []                
            for i in range(len(temp)):
                datalist.append(temp[i]['fields'])
            data = json.dumps(datalist, indent=2, ensure_ascii=False)
            return HttpResponse(data, content_type="application/json")
        except Exception as e:
            return JsonResponse({'message':str(e)},status=HTTPStatus.BAD_REQUEST)
class NoticeDetail(View):
    def get(self, request, noticenum,major):
        try:
            noticedetail = Noti.objects.using('crawled_data').filter(num = noticenum,major_code = major).order_by('-num')
            data = serializers.serialize("json", noticedetail, fields=(
                'num', 'title', 'writer', 'content', 'file_url', 'date', 'img_url'))
            temp = json.loads(data)

            if(temp[0]['fields']['img_url'] == None):
                temp[0]['fields']['img_url'] = [""]
            else:
                temp[0]['fields']['img_url'] = temp[0]['fields']['img_url'].split()
            
            data = temp[0]['fields']
            data['file_url'] = re.sub('{\'','{"',data['file_url'])
            data['file_url'] = re.sub('\':','":',data['file_url'])
            data['file_url'] = re.sub(': \'',':"',data['file_url'])
            data['file_url'] = re.sub('\'}','"}',data['file_url'])

            if(temp[0]['fields']['file_url'] == "[]"):
                temp[0]['fields']['file_url'] = []
                fileList = {}
                fileList['url'] = ""
                fileList['name'] = ""
                temp[0]['fields']['file_url'].append(fileList)
            else:
                fileData = json.loads(data['file_url']) 
            
                urlList = []
                temp[0]['fields']['file_url'] = []
                for i in fileData:
                    urlList += list(i.keys()) 
                for i in range(len(urlList)):
                    fileList = {}
                    fileList['url'] = urlList[i]
                    fileList['name'] = fileData[i].get(urlList[i])
                    temp[0]['fields']['file_url'].append(fileList)
            if(temp[0]['fields']['content'] == None or temp[0]['fields']['content'].replace(" ", "") == ""):
                temp[0]['fields']['content'] = ""

            data = json.dumps(temp[0]['fields'], indent=2, ensure_ascii=False)
            return HttpResponse(content=data)
        except Exception as e:
            return JsonResponse({'message':str(e)},status=HTTPStatus.BAD_REQUEST)
        
        

class NoticeSearch(View):
    def get(self, request, major):
        try:
            keyword = request.GET['keyword']
            searchList = Noti.objects.using('crawled_data').filter(
                title__contains=keyword,major_code = major).order_by('-num')     
            data = serializers.serialize("json", list(
                searchList), fields=('num', 'title', 'date', 'writer'))
            temp = json.loads(data)
            datalist = []
            for i in range(len(temp)):
                datalist.append(temp[i]['fields'])
            data = json.dumps(datalist, indent=2, ensure_ascii=False)
            return HttpResponse(data, content_type="application/json")
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=HTTPStatus.BAD_REQUEST)
        
class scheduleList(View):
    def get(self, request):
        try:
            uSchedule = Schedule.objects.using('crawled_data').all().order_by('id')
            data = serializers.serialize("json", list(
                    uSchedule), fields=('year','month','date','content'))
            data = json.loads(data) 
            itemList = []
            for i in range(len(data)):
                itemList.append(data[i]['fields'])
            data = json.dumps(itemList, indent=2, ensure_ascii=False)
            return HttpResponse(data, content_type="application/json")
        except Exception as e:
            return JsonResponse({'message':str(e)},status=HTTPStatus.BAD_REQUEST)
        
class menuList(View):
    def get(self, request):
        try:
            menuList = Menu.objects.using('crawled_data').all().order_by('date')
            data = serializers.serialize("json", list(
                    menuList), fields=('range','date','restaurant','menu_division','menu_content','etc_info'))
            data = json.loads(data) 
            itemList = []
            for i in range(len(data)):
                itemList.append(data[i]['fields'])
            data = json.dumps(itemList, indent=2, ensure_ascii=False)
            return HttpResponse(data, content_type="application/json")
        except Exception as e:
            return JsonResponse({'message':str(e)},status=HTTPStatus.BAD_REQUEST)