# https://stackoverflow.com/questions/16180428/can-selenium-webdriver-open-browser-windows-silently-in-the-background

from selenium import webdriver
import csv
from datetime import date
from datetime import datetime
import os
import sys
import json
import telebot
from inspect import currentframe

bot = telebot.TeleBot('1844013883:AAEGQdYOdnVYqDk7ugpx9clrWZRJWI9CLkY')

class SiteItem:
    def __init__(self, id, name, price, image = '',discount=0 ):
        self.id = id
        self.name = name
        self.price = price
        self.image=image
        self.discount = discount

    def __str__(self):
        return str((self.id , ', ' , self.name , ', ' , self.price , ';'))

    def __repr__(self):
        return str((self.id , ', ' , self.name , ', ' , self.price , ';'))

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

def getItemsDNS(url):
    PATH = 'C:\Python\chromedriver.exe'
    driver = webdriver.Chrome(PATH)
    driver.get(url)
    driver.implicitly_wait(15)
    search = driver.find_elements_by_xpath("//div[@data-id='product']")
    items = []
    for item in search:
        itemId = item.get_attribute('data-code')
        itemName = item.find_element_by_class_name('catalog-product__name').text
        itemPrice = ''.join(filter(str.isdigit, item.find_element_by_class_name('product-buy__price').text))
        itemDiscount=0
        if (len(itemPrice)>=6):
            itemPriceLen = int(len(itemPrice) / 2)
            oldPrice = itemPrice[itemPriceLen:]
            itemPrice = itemPrice[:itemPriceLen]
            itemDiscount = (int(oldPrice)-int(itemPrice))/int(oldPrice)*100
        if len(itemPrice) > 1:
            items.append(SiteItem(itemId, itemName, itemPrice, discount=itemDiscount))
    driver.quit()
    return items

def getItemsWB(url):
    PATH = 'C:\Python\chromedriver.exe'
    driver = webdriver.Chrome(PATH)
    driver.get(url)
    driver.implicitly_wait(15)
    search = driver.find_elements_by_xpath("//div[@class='dtList-inner']")
    items = []
    for item in search:
        try:
            itemId = item.find_element_by_tag_name("div").get_attribute('id')[1:]
            itemName = item.find_element_by_class_name('goods-name').text + ' ' + item.find_element_by_class_name('brand-name').text
            itemPrice = ''.join(filter(str.isdigit, item.find_element_by_class_name('lower-price').text))
            itemImage =  item.find_element_by_tag_name("img").get_attribute('src')
        except:
            print ('error line ', get_linenumber(),' ', sys.exc_info()[0])
            print(itemId, ' ', itemName, ' ', itemPrice)
        else:
            if len(itemPrice) > 1:
                items.append(SiteItem(itemId, itemName, itemPrice, itemImage))
    driver.quit()
    return items

def getItemsYM(url):
    PATH = 'C:\Python\chromedriver.exe'
    driver = webdriver.Chrome(PATH)
    driver.get(url)
    driver.implicitly_wait(15)
    search = driver.find_elements_by_xpath("//article[@data-autotest-id='product-snippet']")
    items = []
    for item in search:
        try:
            itemId = json.loads(item.get_attribute('data-zone-data'))["id"]
            itemName = item.find_element_by_tag_name('h3').text
            itemPrice = json.loads(item.get_attribute('data-zone-data'))["price"]
            itemDiscount=0
            if ("oldPrice" in json.loads(item.get_attribute('data-zone-data'))):
                itemOldPrice = json.loads(item.get_attribute('data-zone-data'))["oldPrice"]
                itemDiscount = (int(itemOldPrice) - int(itemPrice)) / itemOldPrice * 100
            # print(itemId,' ',itemName,' ',itemPrice)
        except:
            print ('error ', get_linenumber(), ' ', sys.exc_info()[0])
            print(itemId, ' ', itemName, ' ', itemPrice)
        else:
            if type(itemPrice)==int or len(itemPrice) > 1:
                items.append(SiteItem(itemId, itemName, itemPrice,discount=itemDiscount))
    driver.quit()
    return items

def write_csv(data, filename,goodPrice):
    newlines = 0
    if not os.path.isfile(filename):
        my_file = open(filename, "w+")
        my_file.close()
    if os.stat(filename).st_size == 0:
        with open(filename, 'a', encoding='utf8', newline='') as file:
            fields = ['id', 'name', 'price', 'date', 'time']
            writer = csv.writer(file)
            if os.stat(filename).st_size == 0:
                writer.writerow(fields)
                # for item in data:
                #     writer.writerow([item.id, item.name, item.price, date.today(), datetime.now().strftime("%H:%M:%S")])

    with open(filename, 'r', encoding='utf8', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        fileList = list(reader)
        for item in data:
            exists = False
            for fileItem in fileList:
                if item.id == fileItem[0]:       # сюда вписать замену цены в существующих строках иначе будут ошибки
                    try:
                        exists = True
                        if item.price == fileItem[2]:
                            continue
                        if (item.price<fileItem[2]) and round((int(fileItem[2])-int(item.price))/int(fileItem[2])*100)>9:
                            pricedown = ('Цена вниз на ' + item.id + ' ' + item.name+', старая '+ fileItem[2]+ ', новая '+ item.price+ ', падение на '+ str(int(fileItem[2])-int(item.price))+ ' '+str(round((int(fileItem[2])-int(item.price))/int(fileItem[2])*100))+'%')
                            print(pricedown)
                            bot.send_message('277180656', pricedown)
                            if (item.image != ''):
                                bot.send_photo('277180656', item.image)
                        fileItem[2] = item.price
                        fileItem[3] = date.today()
                        fileItem[4] = datetime.now().strftime("%H:%M:%S")
                        continue
                    except:
                        print('error line ', get_linenumber() , ' ',sys.exc_info()[0], ' ', fileItem)
                        continue
            if exists==False:
                fileList.append([item.id,item.name,item.price, date.today(), datetime.now().strftime("%H:%M:%S")])
                # print('New line: ', item)
                newlines+=1
            if (int(item.price)<goodPrice or item.discount > 20):
                pricenew=('!!!!!!!!' + str(item.id) + ' ' + item.name+ ' цена ' + str(item.price))
                bot.send_message('277180656', pricenew)

    with open(filename, 'w', encoding='utf8', newline='') as file:
        # file.truncate(0)
        writer = csv.writer(file)
        writer.writerows(fileList)
    print('data written to ', filename, ' new lines: ', newlines)

def scrap(site, link, filename,maxPages=5,goodPrice=0):
    print('doing',site,filename)
    page = 1
    all_items = []

    while True:
        items=[]
        if (site=='ym'):
            items = getItemsYM(link + str(page))
        if (site=='wb'):
            items = getItemsWB(link + str(page))
        if (site=='dns'):
            items = getItemsDNS(link + str(page))
        if items:
            all_items.extend(items)
            page += 1
            if page > maxPages:
                break
        else:
            break

    print(datetime.now().strftime("%H:%M:%S"), ' Total records: ' + str(len(all_items)))
    write_csv(all_items, filename,goodPrice)


if __name__ == '__main__':
    pass
    # scrap('ym', 'https://market.yandex.ru/catalog--noutbuki-v-anape/54544/list?cpa=0&hid=91013&how=aprice&glfilter=5085102%3A16880592&onstock=1&local-offers-first=0&page=', 'ym-laptops.csv',1,50000)
    # scrap('ym','https://market.yandex.ru/catalog--materinskie-platy-v-anape/55323/list?cpa=0&hid=91020&how=discount_p&glfilter=4923171%3A17781187&onstock=1&local-offers-first=0&page=','ym-mb1200.csv',1)
    # scrap('dns','https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?f[8lf]=evwg-2vyw1-rj64n&p=', 'dns-mb.csv',5)
    # scrap('dns','https://www.dns-shop.ru/catalog/17a8ae4916404e77/televizory/?fr[p2]=50-100&p=','dns-tv.csv',1)
    # scrap('wb','https://www.wildberries.ru/catalog/elektronika/noutbuki-i-kompyutery/komplektuyushchie-dlya-pk?sort=popular&page=','wb-pcparts.csv',1)