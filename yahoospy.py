# -*- coding: utf-8 -*-
import requests
from lxml import html
import datetime
from bs4 import BeautifulSoup
import urllib3

tickers=["MSFT","AAPL","GOOG"]

retrievaldate = datetime.datetime.now()
put= "PUT"
call= "CALL"

def getdata(t):
        # for t in tickers:
        data1 = []
        data2 = []
        http = urllib3.PoolManager()
        url = 'https://au.finance.yahoo.com/quote/' + '{}'.format(t) + '/options'
        print(url)
        data = http.request('GET', url)
        tree = data.data
        soup = BeautifulSoup(tree, 'lxml')
        cat = []
        Date = []
        header = '{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format("Date", "Date Retrieved", "Contract name", "Last trade date","Strike", "Last price",
                                                                               "Bid", "Ask", "Change", "% change","Volume", "Open interest","Implied volatility","Call/Put")
        with open("%s.csv" % t, 'a+') as file:
            file.write(header)
        for y in soup.find_all('option'):
            cat.append(y.get('value'))
            Date.append(y.text)
            print (Date)


        for i, x in zip(cat,Date):
         url = 'https://au.finance.yahoo.com/quote/'+'{}'.format(t)+'/options?date=''{}'.format(i)
         print(url)
         data = requests.get(url)
         tree = html.fromstring(data.content)

        # Calls data
         Cname = tree.xpath('//a[@class="Fz(s) Ell C($c-fuji-blue-1-b)"]/@title')
         Lasttd = tree.xpath('//td[@class="data-col1 Ta(end) Pstart(7px)"]/text()')
         Srate = tree.xpath('//td[@class="data-col2 Ta(end) Pstart(7px)"]/a/text()')
         Lastp = tree.xpath('//table[@class="calls table-bordered W(100%) Pos(r) Bd(0) Pt(0) list-options"]/tbody/tr/td[4]/text()')
         Bid = tree.xpath('//table[@class="calls table-bordered W(100%) Pos(r) Bd(0) Pt(0) list-options"]/tbody/tr/td[5]/text()')
         Ask = tree.xpath('//table[@class="calls table-bordered W(100%) Pos(r) Bd(0) Pt(0) list-options"]/tbody/tr/td[6]/text()')
         Change = tree.xpath('//table[@class="calls table-bordered W(100%) Pos(r) Bd(0) Pt(0) list-options"]/tbody/tr/td[7]/span/text()')
         Perchange = tree.xpath('//table[@class="calls table-bordered W(100%) Pos(r) Bd(0) Pt(0) list-options"]/tbody/tr/td[8]/span/text()')
         Vol = tree.xpath('//table[@class="calls table-bordered W(100%) Pos(r) Bd(0) Pt(0) list-options"]/tbody/tr/td[9]/text()')
         OpenI = tree.xpath('//table[@class="calls table-bordered W(100%) Pos(r) Bd(0) Pt(0) list-options"]/tbody/tr/td[10]/text()')
         Invol = tree.xpath('//table[@class="calls table-bordered W(100%) Pos(r) Bd(0) Pt(0) list-options"]/tbody/tr/td[11]/text()')

        # Puts data
         Pcname = tree.xpath('//table[@class="puts table-bordered W(100%) Pos(r) list-options"]/tbody/tr/td[1]/a/text()')
         Plasttd = tree.xpath('//table[@class="puts table-bordered W(100%) Pos(r) list-options"]/tbody/tr/td[2]/text()')
         Psrate = tree.xpath('//table[@class="puts table-bordered W(100%) Pos(r) list-options"]/tbody/tr/td[3]/a/text()')
         Plastp = tree.xpath('//table[@class="puts table-bordered W(100%) Pos(r) list-options"]/tbody/tr/td[4]/text()')
         Pbid = tree.xpath('//table[@class="puts table-bordered W(100%) Pos(r) list-options"]/tbody/tr/td[5]/text()')
         Pask = tree.xpath('//table[@class="puts table-bordered W(100%) Pos(r) list-options"]/tbody/tr/td[6]/text()')
         Pchange = tree.xpath('//table[@class="puts table-bordered W(100%) Pos(r) list-options"]/tbody/tr/td[7]/span/text()')
         Pperchange = tree.xpath('//table[@class="puts table-bordered W(100%) Pos(r) list-options"]/tbody/tr/td[8]/span/text()')
         Pvol = tree.xpath('//table[@class="puts table-bordered W(100%) Pos(r) list-options"]/tbody/tr/td[9]/text()')
         PopenI = tree.xpath('//table[@class="puts table-bordered W(100%) Pos(r) list-options"]/tbody/tr/td[10]/text()')
         Pinvol = tree.xpath('//table[@class="puts table-bordered W(100%) Pos(r) list-options"]/tbody/tr/td[11]/text()')

         #for calls data saving.

         with open("%s.csv" % t, 'a+') as file:
            for items in zip(Cname, Lasttd, Srate, Lastp, Bid, Ask, Change, Perchange, Vol, OpenI, Invol):

                datawrites = '{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(x, retrievaldate,
                    items[0].replace(',', ''), items[1].replace(',', ''), items[2].replace(',', ''), items[3].replace(',', ''), items[4].replace(',', ''),
                    items[5].replace(',', ''), items[6].replace(',', ''), items[7].replace(',', ''), items[8].replace(',', ''), items[9].replace(',', ''),
                    items[10].replace(',', ''),call)
                file.write(datawrites)
                data1.append(datawrites)
                sdata = ''.join(data1) #coverting list to string
            # for put data saving.

            for items in zip(Pcname, Plasttd, Psrate, Plastp, Pbid, Pask, Pchange, Pperchange, Pvol, PopenI, Pinvol):

                datawrite = '{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
                    x, retrievaldate, items[0].replace(',', ''), items[1].replace(',', ''), items[2].replace(',', ''),
                    items[3].replace(',', ''), items[4].replace(',', ''), items[5].replace(',', ''), items[6].replace(',', ''), items[7].replace(',', ''),
                    items[8].replace(',', ''), items[9].replace(',', ''), items[10].replace(',', ''),put)
                file.write(datawrite)
                data2.append(datawrite)
                sdata2 = ''.join(data2)
         datas = sdata + sdata2
         return datas
for t in tickers:
    result = getdata(t)
    print(result)