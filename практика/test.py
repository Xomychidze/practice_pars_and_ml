import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    with open('output_test.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
    return r.text

def get_href(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    with open('Hrefoutput_test.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
    return r.text


def new_write_csv():
    with open('events_test.csv', 'w', encoding='utf-8', newline='') as f:  # 'w' для перезаписи
        writer = csv.writer(f)
        writer.writerow(['Название', 'Цена (₸)', 'Категория', 'Партнёр', 'Дата'])

def write_csv(data):
    with open('href_test.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)  # каждая строка — список из 3 элементов

def write_csv_row(row):
    with open('events_test.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([row[0], row[1], row[2], row[3], row[4]])

def get_href_data(html):
    soup = BeautifulSoup(html, "lxml")
    data = []
    
    try:
        main_div = soup.find("div", class_="container")
        if main_div is None:
            return "No container found"
        
        # Get attributes with safe fallbacks
        title = str(main_div.get("data-title", "нет названия"))
        price = str(main_div.get("data-minprice", "not price"))
        partner = str(main_div.get("data-partner", "нет partner"))
        category = str(main_div.get("data-category", "нет category"))
        
        add_div = main_div.find('div', class_="event_date_block")
        date = str(add_div.get("data-date", 'No data')) if add_div else 'No data'
        
        data = [title, price, category, partner, date]
        write_csv_row(data)
        return f"{title} | {price} ₸ | {category} | {partner} | {date}"
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return "Error processing data"


def get_data(html):
    soup = BeautifulSoup(html, "lxml")
    
    data = []
    cards = soup.find_all("div", class_="impression-card")
    href_city = soup.find("ul", class_="city-search")
    for card in cards:
        a_tag = card.find("a")
        href = a_tag.get("href")
        data_page = get_href(href)
        need_data = get_href_data(data_page)
        data.append(need_data)
    


    return data



def main():
    page = 1

    while True:
        url = f'https://sxodim.com/aktau/afisha?page=1'
        html = get_html(url)
        parsed = get_data(html)
        if not parsed:
            break
        else:
            print(parsed)
            print(page)
            page += 1

if __name__ == '__main__':
    main()
