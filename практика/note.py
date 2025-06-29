from bs4 import BeautifulSoup


def write_csv(data):
    with open('newplugins.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f) # type: ignore
        writer.writerow(data)

def get_data(html):
    soup = BeautifulSoup(html, "lxml") # type: ignore
    items = soup.find_all("div", class_="impression-card")
    data = []
    for item in items:
        description = item.get_text(strip=True)
        parts = description.split(", ")
        if len(parts) <= 6:
            write_csv(parts)
            data.append(parts)
        else:
            print("⚠️ Incorrect format:", description)
    
    return data



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
        write_csv_row(data) # type: ignore
        return f"{title} | {price} ₸ | {category} | {partner} | {date}"
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return "Error processing data"
