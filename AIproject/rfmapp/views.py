from asyncio.windows_events import NULL
import sys
from django.shortcuts import render
import numpy as np
import pandas as pd
import datetime as dt

from sklearn.cluster import KMeans

from django.db import models

from rfmapp.models import UsersDetails

# Create your views here.
def check_gui(request):

    
    if (request.POST.get('check1') and request.POST.get('check2') and request.POST.get('check3')):
        title1="این گزارش فاقد اعتبار می باشد"
        return render(request, "showAIresult/checkresult.html",{ "title_query":title1})

    elif (request.POST.get('check1') and request.POST.get('check3') ):
        var4_M=request.POST.get('check1')
        Var4_R=request.POST.get('check3')
        title1="مشتریانی که خرید بالا و اخیرا مراجعه نموده اند"
        rfm_R=buys_ai()
        result1=rfm_R[rfm_R['R']==int(Var4_R)]
        result=rfm_R[rfm_R['M']==int(var4_M)]
        result1=result1.reset_index(level=0)
        user_id_list = result1.user.tolist()
        user_id_list=str(tuple(user_id_list))
        query1=UsersDetails.objects.raw('SELECT name, namefamily, email, mobile, bank, account FROM users where id in'+ user_id_list)
        return render(request, "showAIresult/checkresult.html",{"UsersDetails":query1, "title_query":title1})
    elif (request.POST.get('check1') and request.POST.get('check2')):
        var5_M=request.POST.get('check1')
        Var5_F=request.POST.get('check2')
        title1="مشتریانی که حجم خرید بالا و زیاد مراجعه نموده اند"
        rfm_R=buys_ai()
        result1=rfm_R[rfm_R['F']==int(Var5_F)]
        result=rfm_R[rfm_R['M']==int(var5_M)]
        result1=result1.reset_index(level=0)
        user_id_list = result1.user.tolist()
        user_id_list=str(tuple(user_id_list))
        query1=UsersDetails.objects.raw('SELECT name, namefamily, email, mobile, bank, account FROM users where id in'+ user_id_list)
        return render(request, "showAIresult/checkresult.html",{"UsersDetails":query1, "title_query":title1})
    elif (request.POST.get('check2') and request.POST.get('check3')):
        title1="این گزارش فاقد اعتبار می باشد"
        return render(request, "showAIresult/checkresult.html",{ "title_query":title1})
    
    
    elif(request.POST.get('check1')):
        title1="گزارش مشتریانی که بالاترین حجم خرید رو داشتند."
        var1=request.POST.get('check1')
        rfm_new=buys_ai()
        result1=rfm_new[rfm_new['M']==int(var1)]
        result1=result1.reset_index(level=0)
        user_id_list = result1.user.tolist()
        user_id_list=str(tuple(user_id_list))
        query1=UsersDetails.objects.raw('SELECT name, namefamily, email, mobile, bank, account FROM users where id in'+ user_id_list)
        return render(request, "showAIresult/checkresult.html",{"UsersDetails":query1, "title_query":title1})
    elif (request.POST.get('check2')  ) :
        title1="گزارش مشتریانی که بالاترین حجم مراجعه رو داشته اند."
        var2=request.POST.get('check2')
        rfm_new=buys_ai()
        result1=rfm_new[rfm_new['F']==int(var2)]
        result1=result1.reset_index(level=0)
        user_id_list = result1.user.tolist()
        user_id_list=str(tuple(user_id_list))
        query1=UsersDetails.objects.raw('SELECT name, namefamily, email, mobile, bank, account FROM users where id in'+ user_id_list)
        return render(request, "showAIresult/checkresult.html",{"UsersDetails":query1,"title_query":title1})
    elif (request.POST.get('check3') ):
        title1="گزارش مشتریانی که اخیرا مراجعه نموده اند"
        var3=request.POST.get('check3')
        rfm_R=buys_ai()
        result1=rfm_R[rfm_R['R']==int(var3)]
        result1=result1.reset_index(level=0)
        user_id_list = result1.user.tolist()
        user_id_list=str(tuple(user_id_list))
        query1=UsersDetails.objects.raw('SELECT name, namefamily, email, mobile, bank, account FROM users where id in'+ user_id_list)
        return render(request, "showAIresult/checkresult.html",{"UsersDetails":query1, "title_query":title1 })
    
    else:
        msg="please select one of the checkbox for assess your data"
        return render(request, "showAIresult/checkresult.html",{"var1":msg})


def buys_ai():
    data=pd.read_csv('buys.csv')
    data['total_buy']=data['price']*data['size']
    data['updated_at2'] = data['updated_at'].apply(lambda x: pd.to_datetime(x))
    pin_date = max(data['updated_at2']) + dt.timedelta(1)
    rfm = data.groupby('user').agg({
    'updated_at2': lambda x: (pin_date - x.max()).days,
    'order': 'count',
    'total_buy': 'sum'
        })
    rfm.rename(columns= {
    'updated_at2': 'Recency',
    'order': 'Frequency',
    'total_buy': 'Monetary'
    }, inplace=True)
    r_labels = range(4, 0, -1)
    r_groups = pd.qcut(rfm['Recency'], q=4, labels=r_labels)
    f_labels = range(1, 5)
    f_groups = pd.qcut(rfm['Frequency'], q=4, labels=f_labels)
    m_labels = range(1, 5)
    m_groups = pd.qcut(rfm['Monetary'], q=4, labels=m_labels)
    rfm['R'] = r_groups.values
    rfm['F'] = f_groups.values
    rfm['M'] = m_groups.values
    X = rfm[['R', 'F', 'M']]
    kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=300)
    kmeans.fit(X)
    rfm['kmeans_cluster'] = kmeans.labels_
    #Uid_m=rfm[rfm['M']==4]
    return rfm
    #return render(Request, "admin/adminpanel.html",{"data_buy":Uid_m})
