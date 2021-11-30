import time
import schedule
from datetime import datetime
from scrapWithSelenium import scrap

print('running...')
print(datetime.now())


schedule.every(1).hours.do(scrap,'wb','https://www.wildberries.ru/catalog/elektronika/noutbuki-i-kompyutery/komplektuyushchie-dlya-pk?sort=priceup&priceU=110000%3B23998000&page=','wb-pcparts.csv',20)
schedule.every(1).hours.do(scrap,'dns','https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/?f[p3q]=b3ci&p=','dns-laptops.csv',1,55000)
# schedule.every(1).hours.do(scrap,'ym',
#             'https://market.yandex.ru/catalog--noutbuki/54544/list?hid=91013&how=aprice&glfilter=5085102%3A16880592&glfilter=5085119%3A18002970%2C19081250%2C17754601%2C17944473%2C16625219%2C17691566%2C16337183%2C22475370%2C22475390&onstock=1&local-offers-first=0&page=',
#         'ym-laptops.csv',1,55000)
# schedule.every(1).hours.do(scrap,'dns','https://www.dns-shop.ru/search/?q=playstation+5&category=17a8978216404e77&p=','dns-ps5.csv',1)
while True:
    schedule.run_pending()
    time.sleep(1)
