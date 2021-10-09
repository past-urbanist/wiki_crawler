# scrapy crawl citySpiderCSS -o city.json
import scrapy
import re
import json


class citySpiderCSS(scrapy.Spider):
    name = "citySpiderCSS"
    start_urls = list(json.load(open('city_urls.json', 'r')))
    # start_urls = ['https://en.wikipedia.org/wiki/Paris', ]

    def parse(self, response):

        for intro in response.css("table.infobox.geography.vcard"):

            lat, lng = intro.css(
                "span.geo-dec::text").extract_first().split(' ')
            if lat[-1] == 'S':
                lat = '-' + lat
            if lng[-1] == 'W':
                lng = '-' + lng

            brief = response.xpath("string(//p[2])").extract_first()
            brief = re.sub(r'\(.*?\)|\)|\[.*?\]|\n', '', brief)[:1000]
            img = intro.css("img::attr(src)").extract_first()[2:]

            utc = intro.css("a[title*=UTC]::text").extract_first()
            if utc is not None:
                utc = re.sub(r'\:', '.', utc[3:])
                if utc[0] in ('+', '-'):
                    utc = int(float(utc))
                else:
                    utc = 0

            tr_list0 = [re.sub(r' |\,|\n', '', ele)
                        for ele in intro.css("tr *::text").extract()]
            tr_list = [ele for ele in tr_list0 if (
                re.match('[\dA-Za-z].+', ele))]

            nation_pos = \
                -1 if 'Country' not in tr_list else tr_list.index('Country')
            nation = None if nation_pos < 0 else tr_list[nation_pos+1]

            tr_list = [ele for ele in tr_list0 if (
                re.match('[\dAP].+', ele))]
            pop_pos = -1 if 'Population' not in tr_list else tr_list.index(
                'Population')
            pop = re.sub(r'[\D].+', '', tr_list[pop_pos+1])
            area_pos = -1 if 'Area' not in tr_list else tr_list.index('Area')
            area = re.sub(r'[\D].+', '', tr_list[area_pos+1])

            yield {
                'city_name': response.url[30:],
                'img': intro.css("img::attr(src)").extract_first(),
                'lat': float(lat[:-2]),
                'lng': float(lng[:-2]),
                'brief': brief,
                'utc': utc,
                'nation': nation,
                'area': None if area_pos < 0 else float(area),
                'pop': None if pop_pos < 0 else int(pop)
            }
