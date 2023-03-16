from bs4 import BeautifulSoup
import requests
from csv import writer
from random import randint
from time import sleep
import re


url = "https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=2022%2F23;trophy=89;type=season"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
rows = soup.find_all('tr', class_="data1")

link_arr = []
match_ids = []
tvst = []
final_tt =[]
Individual_Teams = []
final_rt =[]

for row in rows:
    links = row.find_all('a')
    tt =[]
    rt = []
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
        
    if((Team1 not in Individual_Teams) or (Team2 not in Individual_Teams)):
        for team in tt:
            if(team not in Individual_Teams):
                Individual_Teams.append(team)
                remaining_team = team
                rt.append(team)
        final_rt.append(rt)         
        link_arr.append(linkText)
        match_ids.append(mids)
        final_tt.append(tt)
    
print(Individual_Teams)
print(final_rt)

with open('dim_players_nehal.csv', 'w', encoding='utf8', newline='') as file:
    thewriter = writer(file)
    header = ['name', 'team', 'image', 'battingStyle', 'bowlingStyle', 'playingRole', 'description']
    thewriter.writerow(header)



    for idx,link in enumerate(link_arr):
        if(idx >= 0):
            inner_url = link
            inner_page = requests.get(inner_url)
            inner_soup = BeautifulSoup(inner_page.content, 'html.parser')

            
            teaminnings = inner_soup.find_all('div', class_=['ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo ds-mb-2', 'ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo ds-opacity-50 ds-mb-2'])
            for teams in teaminnings:
                team = teams.find('span').text
                break
            if(team == 'United Arab Emirates'):
                team = 'U.A.E.'   


            counter = 0
            sce = inner_soup.find_all('tbody', limit=4)
            Final_list = []
            
            for links in sce:               
                
                for ind,link in enumerate(links):
                    
                    if (link.get('class') != ['ds-hidden']):
                        
                        Empty_list = []
                        if (len(link) == 8):

                            # For filtering the teams
                            if(counter == 0 and (team not in final_rt[idx] )):
                                break
                            elif(counter > 0):
                                for i in (0,1):
                                    if(final_tt[idx][i] != team):
                                        sec_batting_team = final_tt[idx][i]
                                if(sec_batting_team not in final_rt[idx] ):
                                    break
                            
                                        
                            for index, flink in enumerate(link):
                                
                                if (index == 0):
                                    '''
                                    /
                                    /
                                    /
                                    '''
                                    # For extracting the name,team and page-link of player
                                    BatsmanName = flink.find('span').text
                                    Empty_list.append(BatsmanName.replace('\xa0', '').replace('â€', '').replace('†', '').replace(',', ''))

                                    if(counter == 0):
                                        Empty_list.append(team)
                                    else:
                                        for i in (0,1):
                                            if(final_tt[idx][i] != team):
                                                Empty_list.append(final_tt[idx][i])
                                                    
                                    playerlink = "https://www.espncricinfo.com" + flink.find('a').get('href')
                                    '''
                                    /
                                    /
                                    /
                                    '''                            
                                    # For extracting the image link of player
                                    newbat = BatsmanName.replace('\xa0', '').replace('†', '').replace('(c)', '').replace(' ','-')
                                    newbat_split = newbat.split("-")
                                    l = len(newbat_split)
                                    new_str = ''
                                    
                                    for i in range(0,l):
                                        if(i==0):
                                            nb_str = newbat_split[i]
                                        elif(i>=2):
                                            nb_str = r'-?\w+?'
                                        else:
                                            nb_str = r'-\w+'
                                        new_str = new_str + nb_str
                                    
                                    text_screener = r'"slug":"' + new_str + r'-?\w+?-page-headshot-cutout-?\d+?'
                                    
                                    player_url = playerlink                                
                                    player_page = requests.get(player_url).text
                                    p = re.compile(text_screener, re.IGNORECASE)
                                    
                                    matches=p.finditer(player_page)
                                    
                                    check = 1
                                    for match in matches:
                                        index1=match.end()
                                        
                                        check=2
                                    

                                    if(check == 2):                                
                                        p_links = player_page[index1: (index1+50)]

                                        pat = re.compile(r"/db/PICTURES/CMS/\d{6}/\d{6}\.?\d?.png", re.IGNORECASE)
                                        matches_new=pat.findall(p_links)
                                        player_img_link = "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_320,q_50/lsci" + matches_new[0]
                                        Empty_list.append(player_img_link)
                                    else:
                                        p = re.compile(r'"\w+-\w+-headshot","url":"', re.IGNORECASE)                                
                                        matches=p.finditer(player_page)
                                    
                                        check = 1
                                        for match in matches:
                                            index1=match.end()
                                            
                                            check=2
                                        if(check == 2):
                                            p_links = player_page[index1: (index1+50)]

                                            pat = re.compile(r"/db/PICTURES/CMS/\d{6}/\d{6}\.?\d?.png", re.IGNORECASE)
                                            matches_new=pat.findall(p_links)
                                            player_img_link = "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_320,q_50/lsci" + matches_new[0]
                                            Empty_list.append(player_img_link)
                                        else:
                                            Empty_list.append('')
                                    # print(check)
                                    '''
                                    /
                                    /
                                    /
                                    '''
                                    # For extracting the details of player
                                    playerid_url = playerlink
                                    playerid_page = requests.get(playerid_url)
                                    playerid_soup = BeautifulSoup(playerid_page.content, 'html.parser')

                                    player_details = playerid_soup.find_all('div', class_='ds-grid lg:ds-grid-cols-3 ds-grid-cols-2 ds-gap-4 ds-mb-8')

                                    for lk in player_details:
                                        cot = 0
                                        for ix,kk in enumerate(lk):
                                                                                        
                                            if(kk.find('p').text == 'Batting Style'):
                                                batting_style = kk.find('span').text
                                                Empty_list.append(batting_style)
                                                cot = 1                                    
                                            elif(kk.find('p').text == 'Bowling Style'):
                                                if(cot == 1):
                                                    bowling_style = kk.find('span').text
                                                    Empty_list.append(bowling_style)
                                                    cot = 2
                                                else:
                                                    Empty_list.append('')
                                                    bowling_style = kk.find('span').text
                                                    Empty_list.append(bowling_style)
                                                    cot = 2
                                            elif(kk.find('p').text == 'Playing Role'):
                                                if(cot == 2):                                                        
                                                    playing_role = kk.find('span').text
                                                    Empty_list.append(playing_role)
                                                    cot=3
                                                else:
                                                    Empty_list.append('')
                                                    playing_role = kk.find('span').text
                                                    Empty_list.append(playing_role)
                                                    cot=3                                         
                                        if(cot != 3):
                                            Empty_list.append('')

                                    player_desc = playerid_soup.find_all('div', class_='ci-player-bio-content')                            
                                    if( player_desc != []):
                                        for i in player_desc:
                                            for j in i:
                                                Empty_list.append(j.text)
                                                break
                                    else:
                                        Empty_list.append('')
                                    '''
                                    /
                                    /
                                    /
                                    '''
                                    thewriter.writerow(Empty_list)
                                     
                        '''
                        /
                        /
                        /
                        '''
                        if(link.get('class') == ['!ds-border-b-0']):
                            a_tags = link.find_all('a')
                            for a_tag in a_tags:
                                '''
                                /
                                /
                                /
                                '''
                                # For extracting the name,team and page-link of player
                                BatsmanName = a_tag.find('span').text
                                Empty_list.append(BatsmanName.replace('\xa0', '').replace('â€', '').replace('†', '').replace(',', ''))
                                
                                if(counter == 0):
                                    Empty_list.append(team)
                                else:
                                    for i in (0,1):
                                        if(final_tt[idx][i] != team):
                                            Empty_list.append(final_tt[idx][i])
                                playerlink = "https://www.espncricinfo.com" + a_tag.get('href')
                                '''
                                /
                                /
                                /
                                '''
                                # For extracting the image link of player                        
                                newbat = BatsmanName.replace('\xa0', '').replace('†', '').replace('(c)', '').replace(' ','-')                        
                                newbat_split = newbat.split("-")
                                l = len(newbat_split)                        
                                new_str = ''
                                
                                for i in range(0,l):
                                    if(i==0):
                                        nb_str = newbat_split[i]
                                    elif(i>=2):
                                        nb_str = r'-?\w+?'
                                    else:
                                        nb_str = r'-\w+'                                
                                    new_str = new_str + nb_str                
                                text_screener = r'"slug":"' + new_str + '-player-page-headshot-cutout'
                                
                                player_url = playerlink
                                player_page = requests.get(player_url).text
                                p = re.compile(text_screener, re.IGNORECASE)
                                matches=p.finditer(player_page)
                                
                                check = 1
                                for match in matches:
                                    index1=match.end()
                                    check=2
                                if(check == 2):                                
                                    p_links = player_page[index1: (index1+50)]

                                    pat = re.compile(r"/db/PICTURES/CMS/\d{6}/\d{6}.png", re.IGNORECASE)
                                    matches_new=pat.findall(p_links)
                                    player_img_link = "https://img1.hscicdn.com/image/upload/f_auto,t_ds_square_w_320,q_50/lsci" + matches_new[0]
                                    Empty_list.append(player_img_link)
                                else:
                                    Empty_list.append('')
                                '''
                                /
                                /
                                /
                                '''
                                # For extracting the details of player
                                playerid_url = playerlink
                                playerid_page = requests.get(playerid_url)
                                playerid_soup = BeautifulSoup(playerid_page.content, 'html.parser')

                                player_details = playerid_soup.find_all('div', class_='ds-grid lg:ds-grid-cols-3 ds-grid-cols-2 ds-gap-4 ds-mb-8')

                                for lk in player_details:
                                    cot = 0
                                    for ix,kk in enumerate(lk):
                                        if(kk.find('p').text == 'Batting Style'):
                                                batting_style = kk.find('span').text
                                                Empty_list.append(batting_style)
                                                cot = 1                                    
                                        elif(kk.find('p').text == 'Bowling Style'):
                                            if(cot == 1):
                                                bowling_style = kk.find('span').text
                                                Empty_list.append(bowling_style)
                                                cot = 2
                                            else:
                                                Empty_list.append('')
                                                bowling_style = kk.find('span').text
                                                Empty_list.append(bowling_style)
                                                cot = 2
                                        elif(kk.find('p').text == 'Playing Role'):
                                            if(cot == 2):                                                        
                                                playing_role = kk.find('span').text
                                                Empty_list.append(playing_role)
                                                cot = 3
                                            else:
                                                Empty_list.append('')
                                                playing_role = kk.find('span').text
                                                Empty_list.append(playing_role)
                                                cot = 3
                                    if(cot != 3):
                                            Empty_list.append('')
                                
                                player_desc = playerid_soup.find_all('div', class_='ci-player-bio-content')                            
                                if( player_desc != []):
                                    for i in player_desc:
                                        for j in i:
                                            Empty_list.append(j.text)
                                            break
                                else:
                                    Empty_list.append('')

                                thewriter.writerow(Empty_list)
                                
                                Empty_list = []
                            
                           
                counter = counter+1
                
                
            
            
    
