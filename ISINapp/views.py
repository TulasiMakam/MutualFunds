import pandas as pd
import datetime
import matplotlib.pyplot as plt
from django.shortcuts import render
from ISINapp.models import MutualFunds
from ISINapp.forms import MutualFundsForm
from matplotlib import pylab
from pylab import *
from io import StringIO
import PIL, PIL.Image
from PIL import Image



def addisin(request):

    isin_list=pd.read_csv('https://amberja.in/wp-content/uploads/2020/01/isin_list.csv', names=['ISIN'],squeeze=True)

    for items in isin_list.iteritems():
        isin_data=pd.read_json('https://my.fisdom.com/api/funds/moreinfoonfund/'+items[1])
        status=str(isin_data['pfwresponse']['status_code'])
        #print("Status code is ",status)

        if status == '200':
            graph_data_for_amfi=isin_data['pfwresponse']['result']['fundinfo']['graph_data_for_amfi']
            legal_name = isin_data['pfwresponse']['result']['fundinfo']['legal_name']
            graph_data = pd.DataFrame(graph_data_for_amfi, columns = ['Date', 'Value'])
            graph_data['Date'] = pd.to_datetime(graph_data['Date'], unit='ms')
            latest_data = graph_data.max()
            #print(legal_name)
            #print(graph_data)
            #graph_data.plot(x ='Date', y='Value', kind = 'line')
            #plt.show()
            MutualFunds_data,created = MutualFunds.objects.update_or_create(ISIN=items[1], mutual_funds_name=legal_name, date = latest_data['Date'], price = latest_data['Value'] , status = status)
            if not created:
	            MutualFunds_data.save()
            print("Database Updated")

        if status == '400':
            date=datetime.datetime.now()
            MutualFunds_data,created = MutualFunds.objects.update_or_create(ISIN=items[1], mutual_funds_name='',date=date, price = 0 ,status = status)
            if not created:
                MutualFunds_data.save()
            print("Data Not found, Database Updated")

    return render(request, 'ISINapp/funds.html')

def mutualfund(request):

    if request.method == 'POST':
        ISIN = request.POST.get('ISIN')

        if MutualFunds.objects.filter(ISIN = ISIN).exists():
            print("ISIN Exists")
            curr_status = MutualFunds.objects.get(ISIN = ISIN)

            if curr_status.status == '200':
                isin_data = pd.read_json('https://my.fisdom.com/api/funds/moreinfoonfund/' + ISIN)
                mutual_funds_name = isin_data['pfwresponse']['result']['fundinfo']['legal_name']
                graph_data_for_amfi = isin_data['pfwresponse']['result']['fundinfo']['graph_data_for_amfi']
                graph_data = pd.DataFrame(graph_data_for_amfi, columns=['Date', 'Value'])
                graph_data['Date']=pd.to_datetime(graph_data['Date'], unit = 'ms').dt.strftime('%d-%b-%Y')
                print(graph_data)
                graph_data.plot(x ='Date', y='Value', kind = 'line')
                #plt.show()
                #fig=my_plot.get_figure()
                print("Fig created")
                my_plot=plt.savefig("static/ISINapp/img.png")
                print("Fig saved")
                return render(request, "ISINapp/success.html", context={'my_plot': my_plot,'ISIN':ISIN, 'mutual_funds_name':mutual_funds_name})

            if curr_status.status == '400':
                print("Values dont exist")
                return render(request, 'ISINapp/failure.html')
        else:
            print("ISIN donot exist")
            return render(request, 'ISINapp/failure.html')

#INF200K01560
