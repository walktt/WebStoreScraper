import time
import schedule
from datetime import datetime
from scrapWithSelenium import scrapDNS
from scrapWithSelenium import scrapWB
from scrapWithSelenium import scrapYM
print('running...')
print(datetime.now())
# scrapDNS('https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?p=','dns-mb.csv')
# scrapWB('https://www.wildberries.ru/catalog/elektronika/noutbuki-i-kompyutery/komplektuyushchie-dlya-pk?sort=popular&page=', 'wb-pc-parts.csv')
# scrapYM('https://market.yandex.ru/catalog--noutbuki-v-anape/54544/list?cpa=0&hid=91013&how=aprice&glfilter=5085102%3A16880592&onstock=1&local-offers-first=0&page=',
#         'ym-laptops.csv')

schedule.every(1).hours.do(scrapDNS,'https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?p=','dns-mb.csv')
schedule.every(1).hours.do(scrapWB,'https://www.wildberries.ru/catalog/elektronika/noutbuki-i-kompyutery/komplektuyushchie-dlya-pk?sort=popular&page=', 'wb-pc-parts.csv')
schedule.every(1).hours.do(scrapDNS,'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/?f[66c]=9mkqp-2681-2680-rouuc-3lh5p-4bpxa&p=','dns-laptops.csv')
# schedule.every(1).hours.do(scrapYM,
#         'https://market.yandex.ru/catalog--noutbuki-v-anape/54544/list?cpa=0&hid=91013&how=aprice&glfilter=5085102%3A16880592&onstock=1&local-offers-first=0&page=',
#         'ym-laptops.csv')
while True:
    schedule.run_pending()
    time.sleep(1)
