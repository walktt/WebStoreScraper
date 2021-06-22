import time
import schedule
from datetime import datetime
from scrapWithSelenium import scrapDNS
from scrapWithSelenium import scrapWB
from apscheduler.schedulers.blocking import BlockingScheduler
print('running...')
print(datetime.now())
# scrapDNS('https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?p=','dns-mb.csv')
# scrapWB('https://www.wildberries.ru/catalog/elektronika/noutbuki-i-kompyutery/komplektuyushchie-dlya-pk?sort=popular&page=', 'wb-pc-parts.csv')
schedule.every(1).hours.do(scrapDNS,'https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?p=','dns-mb.csv')
schedule.every(1).hours.do(scrapWB,'https://www.wildberries.ru/catalog/elektronika/noutbuki-i-kompyutery/komplektuyushchie-dlya-pk?sort=popular&page=', 'wb-pc-parts.csv')
schedule.every(1).hours.do(scrapDNS,'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/?f[66c]=9mkqp-2681-2680-rouuc-3lh5p-4bpxa&p=','dns-laptops.csv')
while True:
    schedule.run_pending()
    time.sleep(1)



#scheduler = BlockingScheduler()
#scheduler.add_job(scrapDNS('https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?p=','dns-mb.csv'), 'interval', hours=3)
#print('1')
#scheduler.start()
#print('2')
