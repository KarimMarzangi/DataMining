from django.shortcuts import render
from surprise import Dataset
from surprise import Reader
import random

from articles.models import Article

from surprise import KNNWithMeans
from django.db import models
import pandas as pd

def articleshow(request):
    #return render(request, 'articles.html')
    articles = Article.objects.all()
    
    return render(request, 'showAIresult/articles.html', {'articles': articles})
def index(request):
    
    return render(request, 'showAIresult/AItest.html')

def getArticleIds(userId):
    df = pd.read_csv('articles/static/datasets/userarticle.csv')
    df1 = df[['uid', 'aid' , 'rate']]
    df1.rename(columns = {'uid':'user', 'aid':'item', 'rate':'rating'}, inplace = True)
    reader = Reader(rating_scale=(0, 5))

    # Loads Pandas dataframe
    data = Dataset.load_from_df(df1[["user", "item", "rating"]], reader)

    sim_options = {
    "name": "cosine",
    "user_based": False,  # Compute  similarities between items
    }
    algo = KNNWithMeans(sim_options=sim_options)

    trainingSet = data.build_full_trainset()

    algo.fit(trainingSet)

    ###########################################333
    a = list(dict.fromkeys(df1[~df1['item'].isin(df1[df1["user"]==userId]['item'])]['item']))
    b=[]
    
    for x in a:
        prediction = algo.predict(userId, x)
        r = prediction.est
        #print(str(x)+ " -> " + str(r))
        b.append({'item':x, 'rating':r })
    c = sorted(b, key = lambda i: i['rating'],reverse=True)

    return c


def articledetail(request, id):
    ar=[]
    c = getArticleIds(3066)
    for i in range(1,4):
        rand_num = random.randrange(1, 10)
        ar.append(c[rand_num]['item'])
    

    article = Article.objects.get(id=id)

    articles = Article.objects.filter(id__in=ar)
    #return HttpResponse(ar)
    #return HttpResponse(showMe())
    return render(request, 'showAIresult/articledetail.html', {'article': article, 'articles': articles})
    #return render(request, 'articledetail.html')

