from bs4 import BeautifulSoup
import requests
from csv import writer

url= "https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=2022%2F23;trophy=89;type=season"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

rows = soup.find_all('tr', class_="data1")

with open('dim_match_summary.csv', 'w', encoding='utf8', newline='') as file:
    thewriter = writer(file)
    header = ['Team 1', 'Team 2', 'Winner', 'Margin', 'Ground', 'Match Date', 'match_id']
    thewriter.writerow(header)
    for row in rows:
        arr = []
        for element in row:
            if element != '\n':
                arr.append(element.get_text())
        thewriter.writerow(arr)        