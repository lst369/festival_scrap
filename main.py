import requests
from bs4 import BeautifulSoup
import lxml
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"    
}
# Collect all fest URLs
fest_url_list = []


# for i in range (0, 144, 24):
for i in range (0, 24, 24):
    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&maxprice=500&o={i}&bannertitle=May"
    
    req = requests.get(url= url, headers=headers)
    json_data = json.loads(req.text)
    html_response = json_data["html"]

    with open (f"scrap_festival/index_{i}.html", "w") as file:
        file.write(html_response)
    
    with open (f"scrap_festival/data/index_{i}.html") as file:
        src = file.read()
 
    soup = BeautifulSoup(src, "lxml")
    cards = soup.find_all("h3")
    

    for item in cards:
        fest_url = "https://www.skiddle.com" + item.find("a").get("href")
        fest_url_list.append(fest_url)

# Collect fest info
filter_fest_date = []

for url in fest_url_list:
    req = requests.get(url=url, headers=headers)

    try:
        soup = BeautifulSoup(req.text)
        fest_info_block = soup.find("div", class_="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-1ik2gjq")
        fest_date = fest_info_block.find(class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol").find_all("span")
        fest_name = soup.find("h1").text.strip()
        for item in fest_date:
            filter_fest_date.append(item.text)
        
        print (filter_fest_date)
        print (fest_name)


    except Exception as ex:
        print(ex)
        print("Damn there was some error ... ")

