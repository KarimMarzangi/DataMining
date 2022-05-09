from curses.ascii import HT
from django.shortcuts import render

from django.http import HttpResponse
from matplotlib import pyplot as plt
import pandas as pd



################################################################################  USER
def getdf1_user():
    df = pd.read_csv('users/static/datasets/users.csv')
    df["day"] = df["created_at"].apply(lambda x:pd.Timestamp(x).date())
    df1 = df.groupby('day').agg({
    'id': 'count',
    })
    df1 = df1.reset_index()
    return df1

def getdf7():
    df1 = getdf1_user()
    df7=[]
    for i in range(0, df1.shape[0]-7, 7):
        s=0
        for j in range(i,i+7):
            #print(df1.iloc[j]['id'])
            s += df1.iloc[j]['id']
        df7.append(s)
    return df7

def fig11(request):
    df1 = getdf1_user()
    fig, ax = plt.subplots()
    df1.hist(ax=ax)
            

    filename = 'f11.png'
    path1 = 'users/static/images/' + filename
    fig.savefig(path1)
    
    msg = 'نشان می دهد اکثر روزها ۳ تا ۵ نفر در روز ثبت نام کرده اند'

    return render(request, 'showAIresult/Burchasespage1.html', {'filename':filename, 'msg':msg})

def fig12(request):
    df1 = getdf1_user()
    plt.figure(figsize=(15,10))
    plt.bar(df1["day"], df1["id"])
    plt.xlabel("Day")
    plt.ylabel("#")
     

    filename = 'f12.png'
    path1 = 'users/static/images/' + filename
    plt.savefig(path1)
    #plt.show()
    msg = ' تعداد ثبت نام مشتری در روز های مختلف'

    return render(request, 'showAIresult/Burchasespage1.html', {'filename':filename, 'msg':msg})


def fig13(request):
    df7 = getdf7()
    plt.figure(figsize=(15,10))
    plt.bar(range(len(df7)), df7)
    plt.xlabel("Week")
    plt.ylabel("#")
    
     
    filename = 'f13.png'
    path1 = 'users/static/images/' + filename
    plt.savefig(path1)
    #plt.show()
    msg = 'تفکیک تعداد ثبت نام مشتری بر حسب هفته های مختلف '

    return render(request, 'showAIresult/Burchasespage1.html', {'filename':filename, 'msg':msg})