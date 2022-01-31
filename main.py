import time
import schedule
from datetime import datetime
from scrapWithSelenium import scrap

# time.sleep(10)

#def scrap(site, link, filename,maxPages=5,goodPrice=0):
# scrap('dns','https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?f[rv35]=13j3sp&p=', 'dns-mb.csv',6)
# scrap('dns','https://www.dns-shop.ru/catalog/17a89c5616404e77/korpusa/?p=', 'dns-case.csv',6)
# scrap('skyscanner','https://www.skyscanner.ru/transport/flights/aaq/mosc/220210/220214/?adults=2&adultsv2=2&cabinclass=economy&children=1&childrenv2=6&destinationentityid=27539438&inboundaltsenabled=false&infants=0&originentityid=27536417&outboundaltsenabled=false&preferdirects=false&preferflexible=false&ref=home&rtn=','skyscanner.csv',1,6000)
scrap('ym',
    'https://market.yandex.ru/catalog--moduli-pamiati-v-krasnodare/26912790/list?glfilter=4898082%3A12109164&glfilter=15937366%3A15937372&hid=191211&how=aprice&onstock=0&local-offers-first=0&page=',
    'ym-mem16.csv',1,3000)
scrap('ym',
    'https://market.yandex.ru/catalog--moduli-pamiati-v-krasnodare/26912790/list?glfilter=4898082%3A12109164&glfilter=15937366%3A15937380&hid=191211&how=aprice&onstock=0&local-offers-first=0&page=',
    'ym-mem8.csv',1,2000)

# schedule.every(1).hours.do(scrap,'wb','https://www.wildberries.ru/catalog/elektronika/noutbuki-i-kompyutery/komplektuyushchie-dlya-pk?sort=priceup&priceU=110000%3B23998000&page=','data/wb-pcparts.csv',20)
schedule.every(2).hours.do(scrap,'dns','https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?f[rv35]=13j3sp&p=', 'dns-mb.csv',6)
schedule.every(3).hours.do(scrap,'dns','https://www.dns-shop.ru/catalog/17a89c5616404e77/korpusa/?p=', 'dns-case.csv',6)
# schedule.every(1).hours.do(scrap,'dns','https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/?f[p3q]=b3ci&p=','dns-laptops.csv',1,55000)
schedule.every(1).hours.do(scrap,'ym',
            'https://market.yandex.ru/catalog--moduli-pamiati-v-krasnodare/26912790/list?glfilter=4898082%3A12109164&glfilter=15937366%3A15937372&hid=191211&how=aprice&onstock=0&local-offers-first=0&page=',
            'ym-laptops.csv',1,3000)
# schedule.every(1).hours.do(scrap,'dns','https://www.dns-shop.ru/search/?q=playstation+5&category=17a8978216404e77&p=','dns-ps5.csv',1)
# schedule.every(1).hours.do(scrap,'skyscanner','https://www.skyscanner.ru/transport/flights/aaq/mosc/220210/220214/?adults=2&adultsv2=2&cabinclass=economy&children=1&childrenv2=6&destinationentityid=27539438&inboundaltsenabled=false&infants=0&originentityid=27536417&outboundaltsenabled=false&preferdirects=false&preferflexible=false&ref=home&rtn=','skyscanner.csv',1,6000)
while True:
    schedule.run_pending()
    time.sleep(1)
