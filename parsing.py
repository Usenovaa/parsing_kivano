'''Введение в веб-скрейпинг. Парсинг'''

'''Парсинг - процесс автоматического сбора данных (с возвожностью записи данных в файл)'''

'''Библиотеки'''
# 1. requests -> отпарвляет запрос на сайт и в итоге получаем html код страницы

# 2. Beautiful Soup -> помогает извлекать информацию из html. Помогает нам обращаться к определенным тегам и вытаскивать информацию.

# 3. lxml -> выступает в роли парсера для Beautiful Soup (разбирает информацию на мелкие части и анализирует данные)

# python3 -m venv venv -> создание виртуального окружения

# source venv/bin/activate 
# (. venv/bin/activate)

# pip3 install -r requirments.txt
import requests
from bs4 import BeautifulSoup
import csv

def write_to_csv(data):
    with open('data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([data['title'], data['price'], data['image']])


def get_html(url):
    '''возвращает html код страницы'''
    response = requests.get(url)
    return response.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    list_page = soup.find('div', class_='pager-wrap').find('ul', class_='pagination pagination-sm').find_all('li')
    last_page = list_page[-1].text
    return int(last_page)


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find('div', class_='list-view').find_all('div', class_='item')
    
    for product in product_list:
        title = product.find('div', class_='listbox_title oh').find('strong').text
        
        price = product.find('div', class_='listbox_price').find('strong').text
        
        image ='https://www.kivano.kg' + product.find('img').get('src')

        dict_ = {'title':title, 'price':price, 'image':image}
        # print(dict_)
        write_to_csv(dict_)
        



def main():
    notebooks_url = 'https://www.kivano.kg/noutbuki'
    pages = '?page='
    html = get_html(notebooks_url)
    number = get_total_pages(html)
    # get_data(html)
    for i in range(1, number+1):
        url_pages = notebooks_url+pages+str(i)
        html = get_html(url_pages)
        get_data(html)

with open('data.csv', 'w') as file:
    write = csv.writer(file)
    write.writerow(['title', 'price', 'image'] )


# main()