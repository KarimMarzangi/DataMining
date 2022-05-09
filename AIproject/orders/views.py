import json
from django.shortcuts import render
from matplotlib import pyplot as plt
import pandas as pd

# Create your views here.

def getdf2_order():
    df = pd.read_csv('orders/static/datasets/orders.csv')
    df["day"] = df["created_at"].apply(lambda x:pd.Timestamp(x).date())
    df1 = df.groupby(['day', 'arz']).agg({
        'id': 'count',
    })
    df1 = df1.reset_index()
    df2 = df1.groupby(['day']).agg({
        'id': 'sum',
    })
    df2 = df2.reset_index()

    return df2

def table5(request):
    df2 = getdf2_order().describe()
  
    json_records = df2.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    msg = 'میانگین و مینیمم و ماکزیمم ثبت سفارش در روز'
    context = {'d': data, 'msg': msg}

    return render(request, 'showAIresult/userorders.html', context)


def fig14(request):
    df2 = getdf2_order()
    plt.figure(figsize=(18,12))
    plt.bar(df2["day"], df2["id"])
    plt.xlabel("Day")
    plt.ylabel("# registers")
  
     
    filename = 'f14.png'
    path1 = 'orders/static/images/' + filename
    plt.savefig(path1)
    ##plt.show()
    msg = 'تعداد ارزهای ثبت شده در روز'

    return render(request, 'showAIresult/Burchasespage1.html', {'filename':filename, 'msg':msg})

def fig15(request):
    df2 = getdf2_order()
    fig, ax = plt.subplots()
    df2.hist(bins=50, ax=ax)
            

    filename = 'f15.png'
    path1 = 'orders/static/images/' + filename
    fig.savefig(path1)
    
    msg = 'بیشتر روزها ۱۸ تا ۳۱ سفارش قرار داده می شود'

    return render(request, 'showAIresult/Burchasespage1.html', {'filename':filename, 'msg':msg})