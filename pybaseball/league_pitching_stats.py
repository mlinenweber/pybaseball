import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_soup(start_dt, end_dt):
	# get most recent standings if date not specified
	if((start_dt is None) or (end_dt is None)):
		print('Error: a date range needs to be specified')
		return None
	url = "http://www.baseball-reference.com/leagues/daily.cgi?user_team=&bust_cache=&type=p&lastndays=7&dates=fromandto&fromandto={}.{}&level=mlb&franch=&stat=&stat_value=0".format(start_dt, end_dt)
	s=requests.get(url).content
	return BeautifulSoup(s, "html.parser")

def get_table(soup):
	table = soup.find_all('table')[0]
	data = []
	headings = [th.get_text() for th in table.find("tr").find_all("th")][1:]
	data.append(headings)
	table_body = table.find('tbody')
	rows = table_body.find_all('tr')
	for row in rows:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    data.append([ele for ele in cols if ele])
	data = pd.DataFrame(data)
	data = data.rename(columns=data.iloc[0])
	data = data.reindex(data.index.drop(0))
	return data

def pitching_stats(start_dt=None, end_dt=None):
	# retrieve html from baseball reference
	soup = get_soup(start_dt, end_dt)
	table = get_table(soup)
	return table


