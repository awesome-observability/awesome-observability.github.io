#!/usr/bin/env python3
# coding: utf-8
import requests
import bs4
from ruamel.yaml import round_trip_dump, round_trip_load


def main():
    with open('articles.yaml') as data_file:
        data = round_trip_load(data_file)


    links = [
        i for i in data['links']
    ]


    missing_title = 0
    for link in links:
        if 'title' in link:
            continue
        missing_title += 1
        try:
            resp = requests.get(link['url'], headers={'User-Agent': 'zoidbergwill-scraper/1.0.0'})
            doc = bs4.BeautifulSoup(resp.content, 'html.parser')
            link['title'] = doc.title.text
            link['description'] = doc.head.findChild('meta', dict(name='description')).attrs['content']
            link['url'] = resp.url
            print(f'Scraped {resp.url}, and found title {link["title"]}')
        except Exception as exc:
            print(f'Failed to scrape {link["url"]}: {exc}')

    data['links'] = links

    with open('articles.yaml', 'w') as data_file:
        data_file.write(round_trip_dump(data))

if __name__ == '__main__':
    main()
