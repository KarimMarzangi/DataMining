import json
from django.shortcuts import render
from datetime import date

from django.http import HttpResponse
from matplotlib import pyplot as plt
import pandas as pd


def getdf1():
    df = pd.read_csv('Burchases/static/datasets/buys.csv')
    df["day"] = df["created_at"].apply(lambda x:pd.Timestamp(x).date())
    df["total"] = df["size"]*df["price"]
    df1 = df.groupby('user').agg({
        'id': 'count',
        'total': 'sum'
    })
    df1 = df1.reset_index()
    df1 = df1.sort_values(by=['id', 'total'], ascending=False)
    return df1
def getdf2():
    df = pd.read_csv('buys.csv')
    df["day"] = df["created_at"].apply(lambda x:pd.Timestamp(x).date())
    df["total"] = df["size"]*df["price"]
    df2 = df.groupby('day').agg({ 'id': 'count','total': 'sum' })
    df2 =df2.reset_index()
    #df2['day'] = df["created_at"]
    return df2

def table1(request,id):
    
    df1 = getdf1()
  
    json_records = df1.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    msg = 'نمایش مشتری ها برحسب تعداد خرید و مبلغ خرید'
    context = {'d': data[0:id], 'msg': msg, 'r': range(10,len(data), 10)}
    return render(request, 'showAIresult/userbuys.html', context)

def table2(request):
    df1 = getdf1().describe()
  
    json_records = df1.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    msg = 'مینیمم و ماکزیمم و میانگین تعداد و مبلغ خرید کاربران '
    context = {'d': data, 'msg': msg}

    return render(request, 'showAIresult/userbuys2.html', context)

def table3(request, id):
    df1 = getdf1()
    df1 = df1.sort_values(by=['total'], ascending=False)

    json_records = df1.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    msg = 'نمایش مشتری ها بر حسب مبلغ خرید'
    context = {'d': data[0:id], 'msg': msg, 'r': range(10,len(data), 10)}

    return render(request, 'showAIresult/userbuys1.html', context)

def table4(request):
    df2 = getdf2()
    df2 = df2.sort_values(by=['id', 'total'], ascending=False)

    json_records = df2.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    msg = 'تعداد خرید در روزهای مختلف همراه با مبلغ'
    context = {'d': data, 'msg': msg}

    return render(request, 'showAIresult/userbuys3.html', context)


def fig5(request):
    df1 = getdf1()
    plt.hist(df1["id"], bins=50)
    plt.xlabel("# repeat")
    plt.ylabel("# people")
    
    filename = 'f5.png'
    path1 = 'burchases/static/images/' + filename
    plt.savefig(path1)
    #plt.show()
    msg = 'مشتری ها حداقل ۲ بار  حداکثر ۲۱ بار خرید کرده اند و همچنین نشان می دهد که بیشتر مشتری های ما ۹ تا ۱۱ بار خرید نموده اند'

    return render(request, 'showAIresult/Burchasespage1.html', {'filename':filename, 'msg':msg})

def fig8(request):
    df1 = getdf1()
    plt.hist(df1["total"], bins=10)
    plt.xlabel("price")
    plt.ylabel("#")
    

    filename = 'f8.png'
    path1 = 'burchases/static/images/' + filename
    plt.savefig(path1)
    #plt.show()
    msg = 'نشان می دهد که بیشترین معاملات دارای چه حجمی بوده است همچنین نشان می دد که تعداد مشتری ها با حجم معاملاتی بالا خیلی کم می باشد'

    return render(request, 'showAIresult/Burchasespage1.html', {'filename':filename, 'msg':msg})

def fig9(request):
    df2 = getdf2()
    plt.figure(figsize=(15,10))
    plt.bar(df2["day"], df2["id"])
    plt.xlabel("Day")
    plt.ylabel("#")
  

    filename = 'f9.png'
    path1 = 'burchases/static/images/' + filename
    plt.savefig(path1)
    #plt.show()
    msg = 'نمودار تعداد فروش در روزهای مختلف'

    return render(request, 'showAIresult/Burchasespage1.html', {'filename':filename, 'msg':msg})


def fig10(request):
    df2 = getdf2()
    plt.figure(figsize=(15,10))
    plt.bar(df2["day"], df2["total"])
    plt.xlabel("Day")
    plt.ylabel("$$$")
    

    filename = 'f10.png'
    path1 = 'burchases/static/images/' + filename
    plt.savefig(path1)
    #plt.show()
    msg = 'نمودار حجم فروش در روزهای مختلف'

    return render(request, 'showAIresult/Burchasespage1.html', {'filename':filename, 'msg':msg})
