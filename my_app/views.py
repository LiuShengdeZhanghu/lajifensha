from django.shortcuts import render
from django.http import JsonResponse
from .models import Anli
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import my_app.DataAnalysis as DataAnalysis
import my_app.KeyWord as KeyWord
import my_app.sim_calByCenter as simCenter
import json
import time
# Create your views here.

def index(request):
    return render(request,"search.html")

def dataku(request):
    return render(request,"DataKu.html")

def beiyeshi(request):
    return render(request,"BeiYeShi.html")
def process(request):
    return render(request,'process.html')
def introduce(request):
    return render(request,'introduce2.html')

def anliserch(request):
    title = request.GET.get("title")
    address = request.GET.get("address")
    datetime = request.GET.get("datetime")
    anli=None
    #如果什么都不输入，就查询全部案例
    if title == "" and address == "" and datetime == "":
        anli = Anli.objects.all()
        res_list=[]
        for an in anli:
            res_list.append({"id":an.id,"time":an.anli_time,"city":an.city,"title":an.title,"result":an.result,"point":an.point})

        return JsonResponse(res_list,safe=False)
    #有条件的进行查询
    if title !="":
        anli = Anli.objects.filter(title__contains=title.strip())
    if address !="":
        if anli !=None:
            anli = anli.filter(city__contains=address.strip())
        else:
            anli = Anli.objects.filter(city__contains=address.strip())
    if datetime !="":
        if anli !=None:
            anli = anli.filter(anli_time__year=datetime.strip())
        else:
            anli =Anli.objects.filter(anli_time__year=datetime.strip())
    if anli !=None:
        res_list=[]
        for an in anli:
            res_list.append({"id":an.id,"time":an.anli_time,"city":an.city,"title":an.title,"result":an.result,"point":an.point})
        return JsonResponse(res_list,safe=False)
    else:
        res_list=[]
        return JsonResponse(res_list,safe=False)

def anliDetail(request):
    id = request.GET.get("id")
    try:
        anli = Anli.objects.get(pk=int(id))
        dic = {"code": 1, "content": anli.content}
    except Exception as e:
        dic = {"code":0,"content":"没有查询到相关案例的经历"}
    return JsonResponse(dic,safe=False)

#屏蔽掉验证
@csrf_exempt
def anliAnalysis(request):
    if request.method == 'POST':
        data = dict(request.POST)["key_string"][0]
        da = DataAnalysis.Vectorization()
        format_matrix = da.get_format_matrix(data)
        sim_dict = da.get_similarity_vector(format_matrix)
        case_description = da.get_case(sim_dict['max_sim'])
        img_dict = da.get_img(sim_dict['max_sim'])
        suggest_dict = da.get_suggest(sim_dict['max_sim'])
        order_str = da.get_order()
        format_dict = formatmatrix_to_dict(format_matrix)
        json_str = json.dumps({'format_dict': format_dict, 'sim_dict': sim_dict, 'case_description': case_description,
                               'img_dict': img_dict, 'suggest_dict': suggest_dict, 'order_str': order_str,
                               'status_code': str(200), 'status_msg': '(^_^)'})
        time.sleep(1)

        return JsonResponse(json_str,safe=False)
    rt_dict = {'code': str(200), 'msg': 'cg'}
    return JsonResponse(rt_dict,safe=False)

def formatmatrix_to_dict(format_matrix):
    format_matrix_dict = {}
    for fmt_li in format_matrix:
        temp_str = ''
        for block in fmt_li[1:]:
            temp_str = temp_str + '-' + block[0:6]
        format_matrix_dict[fmt_li[0]] = temp_str
    return format_matrix_dict

@csrf_exempt
def baiyeshiAnli(request):
    if request.method == 'POST':
        data = request.POST["txt"]
        kw = KeyWord.KeyWord()
        rt_list = kw.TF_IDFKeyWord(data)
        word_to_text = kw.data_prepare(data)
        sC = simCenter.sim_calByCenter()
        text_type = sC.cosine_dis(word_to_text)
        rt_dic={"keywords":rt_list,"type":text_type,"textvalue":word_to_text[0:20]}
        print(rt_dic)
        return JsonResponse(rt_dic,safe=False)
    rt_dic = {"content":"cg"}
    return JsonResponse(rt_dic,safe=False)