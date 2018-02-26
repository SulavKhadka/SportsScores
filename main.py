import requests
from bs4 import BeautifulSoup
from pprint import pprint

def partial_href_link_search(page_section, href_content):
	game_status = page_section.select('a[href^="{}"]'.format(href_content))
	if game_status:
		return [game_status[0]['href']]
	else:
		return []


def get_page(page_link):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	response = requests.get(page_link, headers=headers)
	return response


def get_matchup(page_link):

	page_stats = {}

	response = get_page(page_link)
	if response.status_code == 200:

		sub_section = BeautifulSoup(response.text, 'html.parser')

		# Page Title
		page_title = sub_section.find("title").text
		page_stats["Title"] = page_title

		score_section = sub_section.find("div", {"class": "clearfix score-container"}).find("div", {"class": "teams"})

		# Game Status
		status = score_section.find("div", {"class": "tile-game-heading"})
		if status:
			page_stats["status"] = status.text.split(" - ")[-1].strip()
		else:
			page_stats["status"] = ""

		# Get Teams
		teams = score_section.find_all("div", {"class": "media"})
		team_counter = 1
		for i in teams:
			city = i.find_all("div")
			for j in city:
				team_city = j.find("div", {"class": "team-city"})
				team_name = j.find("a", {"class": "desktop-name"})
				record = j.find("span", {"class": "record"})
				if team_city:
					team_key = "team {}".format(team_counter)
					page_stats[team_key] = {"city": team_city.find("a").text.strip(),
					                      "name":team_name.find("span").text.strip(),
					                      "record": record.text.strip()}
					team_counter += 1

					# print("+++++++++++++++++++++++++++++++++++")
					# print("{} {}: {}".format(team_city.find("a").text.strip(), team_name.find("span").text.strip(), record.text.strip()))
					# print("+++++++++++++++++++++++++++++++++++")
	return page_stats


def main():
	sport = "college-football"
	page_link = "https://www.si.com/{}/scoreboard".format(sport)
	response = get_page(page_link)

	if response.status_code == 200:
		sub_section = BeautifulSoup(response.text, 'html.parser')
		score_section = sub_section.find("div", {"class": "content"})
		page_title = score_section.find("h1", {"class": "page-title"}).text
		print(page_title)
		scores = score_section.find_all("div", {"class": "clearfix"})
		for i in scores:
			game_status = partial_href_link_search(i, "/{}/game/".format(sport))
			if game_status:
				url = "https://www.si.com{}".format(game_status[0])
				print(url)
				pprint(get_matchup(url))
				input("HIHIHIHIHIHIHIHIH")




main()

