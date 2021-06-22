import requests
import csv
from bs4 import BeautifulSoup
import re

class SiteItem:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
    def __str__(self):
        return (self.id+', '+self.name+', '+self.price)
    def __repr__(self):
        return (self.id+', '+self.name+', '+self.price)

def write_csv(data):
    with open('result.csv','a',newline='') as file:
        fields = ['id','name','price']
        #writer=csv.DictWriter(f,fieldnames=fields)
        #writer.writerow(data)
        writer = csv.writer(file)
        writer.writerow(fields)
        for item in data:
            writer.writerow([item.id,item.name,item.price])

def get_html(url):
    response = requests.get(url)
    if not response.ok:
        print(f'Code: {response.status_code}, url: {url}')
    return response.text


def get_items(html):
    soup = BeautifulSoup(html, 'lxml')
    # ищем цены и id и заголовки - ситилинк
    s_items = soup.find_all('div', {
        'class': 'product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist'})
    items = []
    for item in s_items:
        items.append(SiteItem(item.get('data-product-id'),
                              item.find('a', {'class': 'ProductCardHorizontal__title'}, 'title').get('title'),
                              item.get('data-price')))
    #print(items)
    return items


def main():
    all_items = []
    start = 1
    url = f'https://www.citilink.ru/catalog/ssd-nakopiteli/?p={start}'

    while True:
        items = get_items(get_html(url))
        if items:
            all_items.extend(items)
            start += 1
            print(start)
            url = f'https://www.citilink.ru/catalog/ssd-nakopiteli/?p={start}'
        else:
            break
    print(len(all_items))
    write_csv(all_items)


if __name__ == '__main__':
    main()
