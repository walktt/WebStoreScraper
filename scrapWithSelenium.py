from selenium import webdriver
import csv
from datetime import date
from datetime import datetime
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


# https://stackoverflow.com/questions/16180428/can-selenium-webdriver-open-browser-windows-silently-in-the-background


class SiteItem:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def __str__(self):
        return (self.id + ', ' + self.name + ', ' + self.price + ';')

    def __repr__(self):
        return (self.id + ', ' + self.name + ', ' + self.price + ';')


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
        if len(itemPrice) > 1:
            items.append(SiteItem(itemId, itemName, itemPrice))
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
            # print(itemId,' ',itemName,' ',itemPrice)
        except:
            print ('error')
        else:
            if len(itemPrice) > 1:
                items.append(SiteItem(itemId, itemName, itemPrice))
    driver.quit()
    return items

def write_csv(data, filename):
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
                for item in data:
                    writer.writerow([item.id, item.name, item.price, date.today(), datetime.now().strftime("%H:%M:%S")])
    else:
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
                            if (item.price<fileItem[2]) and round((int(fileItem[2])-int(item.price))/int(fileItem[2])*100)>5:
                                print ('Цена вниз на ' , item.id , ' ' , item.name,', старая ', fileItem[2], ', новая ', item.price, ', падение на ', int(fileItem[2])-int(item.price), ' ',round((int(fileItem[2])-int(item.price))/int(fileItem[2])*100),'%')
                            fileItem[2] = item.price
                            fileItem[3] = date.today()
                            fileItem[4] = datetime.now().strftime("%H:%M:%S")
                            continue
                        except:
                            print('line 95 error - ' , fileItem)
                            continue
                if exists==False:
                    fileList.append([item.id,item.name,item.price])
                    print('New line: ', item)
                    newlines+=1

        with open(filename, 'w', encoding='utf8', newline='') as file:
            # file.truncate(0)
            writer = csv.writer(file)
            writer.writerows(fileList)
    print('data written to ', filename, ' new lines: ', newlines)

def scrapDNS(link, filename):
    # link = 'https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?p='
    page = 1
    all_items = []

    while True:
        items = getItemsDNS(link + str(page))
        if items:
            all_items.extend(items)
            page += 1
            if page > 20:
                break
        else:
            break

    print('Total records: ' + str(len(all_items)))
    write_csv(all_items, filename)

def scrapWB(link, filename):
    page = 1
    all_items = []

    while True:
        items = getItemsWB(link + str(page))
        if items:
            all_items.extend(items)
            page += 1
            if page > 20:
                break
        else:
            break

    print(datetime.now().strftime("%H:%M:%S"), ' Total records: ' + str(len(all_items)))
    write_csv(all_items, filename)

# if __name__ == '__main__':
    # scrapDNS('https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?p=', 'dns-mb-test1.csv')
    # scrapWB('https://www.wildberries.ru/catalog/elektronika/noutbuki-i-kompyutery/komplektuyushchie-dlya-pk?sort=popular&page=1','test.csv')