from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
from collections import defaultdict
import pandas as pd
import pickle

pd.set_option('display.max_columns', None)

class Spider:
    """
    This class is created based on two diaries, it is not optimized
    for working with any web site.
    """

    def __init__(self, start_url: str, key_words: list):
        self.start_url = start_url
        self.current_url = start_url
        self.key_words_to_search = key_words
        self.media_found = []

    def _get_formated_html(self, url):
        try:
            html = urlopen(url)

            bs = BeautifulSoup(html.read(), 'html.parser')
            return bs
        except:
            return None


    def _get_country_href(self, bs):
        try:
            countries_href = {}
            for a in bs.find_all('a', href=True):
                if a.text in countries and re.match(r"/world-media-directory*", a['href']):

                    countries_href[a.text] = self.start_url + a['href'].split('/world-media-directory/')[1]

            return countries_href
        except AttributeError as e:
            return None

    def _get_hrefs_media_from_href_country(self, href_country):
        try:
            bs = self._get_formated_html(href_country)
            test = bs.find_all('div', {"data-media": True})
            media_info = {}
            for t in test:
                diario = t.find_all("a", href=True)[0].text
                media_href = self.start_url + t.find_all("a", href=True)[0]['href'].split('/world-media-directory/')[1]
                media_info[media_href] = diario


                # break # this one is for testing just one url


            return  media_info
        except AttributeError as e:
            return None


    def _get_media_url(self, media_href, media):
        try:
            bs = self._get_formated_html(media_href)
            test = bs.find_all('tr')

            for t in test:
                if len(t.find_all('th')) > 0 and t.find_all('th')[0].text == "Front Page URL":
                    media_url = t.find_all('a')[0]['href']
                    twitter_account = self._get_twitter_account(media_url)
                    break

            return {"media": media, "url": media_url, "twitter_account": twitter_account}
        except AttributeError as e:
            return None


    def _get_twitter_account(self, news_url):
        try:
            bs = self._get_formated_html(news_url)
            links = bs.find_all('a', href=True)

            for link in links:
                if re.match(r'https?://(www\.)?twitter\.com/*', link['href']) and 'share' not in link['href']:
                    return link['href']
                    break

        except AttributeError as e:
            return None


    def start_crawling(self):
        print("Crawling started.")
        bs = self._get_formated_html(self.current_url)
        country_hrefs = self._get_country_href(bs) if bs is not None else None

        print('  Getting news media data...')

        if bs and country_hrefs:
            for country, country_href in country_hrefs.items():
                media_href_dict = self._get_hrefs_media_from_href_country(country_href)
                list_of_media_info = []
                for media_href, media in media_href_dict.items():
                    list_of_media_info.append(self._get_media_url(media_href, media))
                self.media_found.append({"country": country, "media_news_data": list_of_media_info})

        print('  News media retrieved.')

    def save_data(self, filename):
        df = self.transform_json_to_dataframe(self.media_found)
        with open('../data/' + filename + '.p', 'wb') as fp:
            pickle.dump(df, fp)

        print('  File with new media generated.')

        self.save_json_for_review(filename)


    def save_json_for_review(self, file_name):
        with open(file_name + '.json', 'w', encoding='utf-8') as f:
            json.dump(self.media_found, f, ensure_ascii=False, indent=4)


    def transform_json_to_dataframe(self, json):
        data_dict = defaultdict(list)
        for country_data in json:
            for register in country_data['media_news_data']:
                if register['twitter_account']:
                    data_dict['country'].append(country_data['country'])
                    data_dict['media'].append(register['media'])
                    data_dict['url'].append(register['url'])
                    data_dict['twitter_account'].append(register['twitter_account'])

        return pd.DataFrame(data_dict)


# countries = ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Paraguay", "Peru", "Uruguay", "Venezuela"]
countries = ["Ecuador"]


url = 'https://www.einpresswire.com/world-media-directory/'

peter = Spider(url, countries)
peter.start_crawling()

peter.save_data('media_news')
