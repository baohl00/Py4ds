import requests 
from bs4 import BeautifulSoup as soup
import pandas as pd
from os.path import join

def doc_url(url):
    rq = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}) 
    return soup(rq.text)

def crawl_data(url):
    dict_tr={}
    dict_tr['Player']=[]
    dict_tr['Market_value(m)'] =[]
    dict_tr['Position']=[]
    dict_tr['Age']=[]
    dict_tr['Nationality'] =[]
    dict_tr['Club']=[]
    for idx in range(1,5):
        path_url=join(url,str(idx))
        doc = doc_url(path_url)
        elements=doc.find(id="yw1").find("table", {"class":"items"}).find_all('td',{"class": "hauptlink"})
        i= 0
        for element in elements:
            if i%2!=1:
                dict_tr['Player'].append(element.get_text().replace('\n',''))
            else:dict_tr['Market_value(m)'].append(float(element.get_text().replace('€','').replace('m','')))
            i=i+1
        elements=doc.find(id="yw1").find("table", {"class":"items"}).find_all('table',{"class": "inline-table"})
        for element in elements:
            dict_tr['Position'].append(element.get_text())
        
        elements=doc.find(id="yw1").find("table", {"class":"items"}).find("tbody")
        temp2=elements.find_all("td",{"class":"zentriert"})
        count = 0
        for i in temp2:
            if count ==1:
                #contry
                dict_tr['Nationality'].append(i.find("img").get('title'))
                count= count+1
            elif count ==2:
                #age
                dict_tr['Age'].append(int(i.get_text()))
                count= count+1
            elif count ==3:
                #clb
                dict_tr['Club'].append(i.find("a").get('title'))
                count =0
            else:
                count= count+1
    return dict_tr

#PREMIER_LEAGUE
url ='https://www.transfermarkt.com/premier-league/marktwerte/wettbewerb/GB1/ajax/yw1/page/'
pd.DataFrame(crawl_data(url)).to_csv('eng_2012.csv', index = False)

#LALIGA

url = 'https://www.transfermarkt.com/jumplist/marktwerte/wettbewerb/ES1/ajax/yw1/page/'
pd.DataFrame(crawl_data(url)).to_csv('spa_2012.csv', index = False)

#SERIE_A

url = 'https://www.transfermarkt.com/serie-a/marktwerte/wettbewerb/IT1/page/'
pd.DataFrame(crawl_data(url)).to_csv('ita_2012.csv', index = False)

#BUNDESLIGA

url = 'https://www.transfermarkt.com/bundesliga/marktwerte/wettbewerb/L1/page/'
pd.DataFrame(crawl_data(url)).to_csv('ger_2012.csv', index = False)

#LIGUE_1

url = 'https://www.transfermarkt.com/ligue-1/marktwerte/wettbewerb/FR1/page/'
pd.DataFrame(crawl_data(url)).to_csv('fra_2012.csv', index = False)