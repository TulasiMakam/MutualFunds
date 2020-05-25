from celery.schedules import crontab
from celery.task import periodic_task
import pandas as pd
import datetime
from ISINapp.models import MutualFunds

@periodic_task(run_every=crontab(minute=0, hour='12,23'))
def periodic_task():
    isin_list=pd.read_csv('https://amberja.in/wp-content/uploads/2020/01/isin_list.csv', names=['ISIN'],squeeze=True)
    for items in isin_list.iteritems():
        isin_data=pd.read_json('https://my.fisdom.com/api/funds/moreinfoonfund/'+items[1])
        status=str(isin_data['pfwresponse']['status_code'])
        if status == '200':
            graph_data_for_amfi=isin_data['pfwresponse']['result']['fundinfo']['graph_data_for_amfi']
            legal_name = isin_data['pfwresponse']['result']['fundinfo']['legal_name']
            graph_data = pd.DataFrame(graph_data_for_amfi, columns = ['Date', 'Value'])
            graph_data['Date'] = pd.to_datetime(graph_data['Date'], unit='ms')
            latest_data = graph_data.max()
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