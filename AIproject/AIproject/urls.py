"""AIproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Burchases import views as bviews
from Users import views as uviews
from orders import views as oviews
from articles import views as aviews
from rfmapp import views as rviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', aviews.index),
    ###########################################33  Burchases
    path('burchases/table1/<int:id>/', bviews.table1, name='table1'),
    path('burchases/table2/', bviews.table2, name='table2'),
    path('burchases/table3/<int:id>/', bviews.table3, name='table3'),
    path('burchases/table4/', bviews.table4, name='table4'),

    path('burchases/fig5/', bviews.fig5, name='fig5'),

    path('burchases/fig8/', bviews.fig8, name='fig8'),
    path('burchases/fig9/', bviews.fig9, name='fig9'),
    path('burchases/fig10/', bviews.fig10, name='fig10'),


    ###########################################33  Users
    path('users/fig11/', uviews.fig11, name='fig11'),
    path('users/fig12/', uviews.fig12, name='fig12'),
    path('users/fig13/', uviews.fig13, name='fig13'),

    ###########################################################  ORDERS
    path('orders/fig14/', oviews.fig14, name='fig14'),
    path('orders/fig15/', oviews.fig15, name='fig15'),
    path('orders/table5/', oviews.table5, name='table5'),
    ###########################################################  Article
    path('article/',aviews.articleshow, name='articleshow'),    

    path('articledetail/<int:id>/',aviews.articledetail, name='articledetail'),    

    ############################################################# RFM

    path('rfm/rfmmodel/', rviews.check_gui),




]
