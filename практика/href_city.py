from html import unescape
import json
import requests
from bs4 import BeautifulSoup
import csv
import practice as pr
from image_delete import delete_image

def get_html(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    with open('output_href_city.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
    return r.text

def new_write_csv():
    with open('href.csv', 'w', encoding='utf-8', newline='') as f:  # 'w' для перезаписи
        writer = csv.writer(f)
        writer.writerow(['href'])

def write_csv_row(row):
    with open('href.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([row])
def save_cities_raw_json(html, filename='cities_full.json'):
    soup = BeautifulSoup(html, "lxml")
    ul_tag = soup.find("ul", class_="select-city-list")
    if not ul_tag:
        print("❌ Не найден блок с городами")
        return

    data_cities_raw = ul_tag.get("data-cities")
    if not data_cities_raw:
        print("❌ Атрибут data-cities отсутствует")
        return

    data_cities_json = unescape(data_cities_raw)
    cities = json.loads(data_cities_json)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(cities, f, ensure_ascii=False, indent=4)
    print(f"✅ Сохранено {len(cities)} городов в {filename}")

def get_data(html):
    soup = BeautifulSoup(html, "lxml")
    data = []

    ul_tag = soup.find("ul", class_="select-city-list")
    if ul_tag is None:
        print("❌ Не найден <ul class='select-city-list'>")
        return []

    data_cities_raw = ul_tag.get("data-cities")
    if not data_cities_raw:
        print("❌ Атрибут data-cities не найден")
        return []

    # Распаковка HTML-escaped строки
    data_cities_json = unescape(data_cities_raw)

    # Преобразуем в список словарей
    cities = json.loads(data_cities_json)

    for city in cities:
        slug = city.get("slug")
        if slug:
            href : str = f"https://sxodim.com/{slug}/"
            pr.main(href, slug)
            print(f"✅ Найден город: {slug} -> {href}")
            write_csv_row(href)
            data.append(href)

    return data


def main():
    page = 1
    try:
        ans = int(input("Do you want to restart filling out the CSV file?\nWrite number:\n1. Yes\n2. No\n"))
        if ans == 1:
            new_write_csv()
            pr.new_write_csv()
            delete_image()
        else:
            print("Okay")
    except ValueError:
        print("Please enter a valid number (1 or 2).")

    url = f'https://sxodim.com/'
    html = get_html(url)
    parsed = get_data(html)
    save_cities_raw_json(html)
    print(parsed)
        

if __name__ == '__main__':
    main()
