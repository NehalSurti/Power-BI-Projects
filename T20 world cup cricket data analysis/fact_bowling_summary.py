from bs4 import BeautifulSoup
import requests
from csv import writer
from random import randint
from time import sleep

url = "https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=2022%2F23;trophy=89;type=season"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
rows = soup.find_all('tr', class_="data1")

link_arr = []
match_ids = []
tvst = []
final_tt =[]

for row in rows:
    links = row.find_all('a')
    tt =[]
    for index, link in enumerate(links):
        if(index == 0):
            Team1 = link.text
            tt.append(Team1)
        elif(index == 1):
            Team2 = link.text
            tt.append(Team2)
        else:
            linkText = "https://stats.espncricinfo.com" + link.get('href')
            mids = link.text
        
    link_arr.append(linkText)
    match_ids.append(mids)
    tvst.append(Team1+' Vs '+Team2)
    final_tt.append(tt)
    

with open('fact_bowling_summary_nehal.csv', 'w', encoding='utf8', newline='') as file:
    thewriter = writer(file)
    header = ['match', 'bowlingTeam', 'bowlerName', 'overs', 'maiden', 'runs', 'wickets','economy','0s','4s','6s','wides','noBalls','match_id']
    thewriter.writerow(header)


    for idx,link in enumerate(link_arr):
        inner_url = link
        inner_page = requests.get(inner_url)
        inner_soup = BeautifulSoup(inner_page.content, 'html.parser')

        match_id = match_ids[idx]
        match = tvst[idx]


        teaminnings = inner_soup.find_all('div', class_=['ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo ds-mb-2', 'ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo ds-opacity-50 ds-mb-2'])
        for teams in teaminnings:
            team = teams.find('span').text
            # print(team)
            break
        if(team == 'United Arab Emirates'):
            team = 'U.A.E.'   


        counter = 0
        sce = inner_soup.find_all('tbody', limit=4)
        Final_list = []
        
        for links in sce:
            
            
            for ind,link in enumerate(links):

                if (link.get('class') != ['ds-hidden']):

                    if (len(link) == 11):
                        
                        Empty_list = []
                        Empty_list.append(match)
                        if(counter == 1):
                            for i in (0,1):
                                if(final_tt[idx][i] != team):
                                    Empty_list.append(final_tt[idx][i])
                        else:
                            Empty_list.append(team)
                                                
                        for index, flink in enumerate(link):

                            if (index == 0):
                                bowlerName = flink.find('span').text
                                Empty_list.append(bowlerName.replace('\xa0', ''))
                            elif (index == 4):
                                if(len(flink)>1):
                                    wickets = flink.find('span').text
                                    Empty_list.append(wickets)
                                else:
                                    Empty_list.append(flink.text)
                            else:
                                Empty_list.append(flink.text)
                            
                        Empty_list.append(match_id)
                        
                        thewriter.writerow(Empty_list)
                        
                
            counter = counter+1
            
        

