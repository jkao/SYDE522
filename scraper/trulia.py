from bs4 import BeautifulSoup

import json
import re

import urllib
import urllib2

# Trulia Search URL
BASE_TRULIA_SEARCH_URL = "http://www.trulia.com/for_sale/%s/%s_p"
DEFAULT_LOCATION = "San_Francisco,CA"


class TruliaScraper(object):
    def truliaSearchURL(self, location=DEFAULT_LOCATION, page=1):
        return (BASE_TRULIA_SEARCH_URL % (location, page))

    def scrapePage(self, pageNum):
        return urllib2.urlopen(
            self.truliaSearchURL(page=pageNum)).read()

    def extractAttributes(self, articleXML):
        # Id
        uid = articleXML["data-property-id"]
        print("uid %s " % uid)

        # URL
        url = ("http://www.trulia.com%s" %
               articleXML.find("a", "propertyImageLink")["href"])
        print("url %s " % url)

        # Address
        address = articleXML.find("meta", itemprop="streetAddress")["content"]
        print("address %s " % address)

        # Latitude & Longitude
        latitude = articleXML.find("meta", itemprop="latitude")["content"]
        longitude = articleXML.find("meta", itemprop="longitude")["content"]
        print("latitude, longitude: %s %s" % (latitude, longitude))

        # Photo Count
        photoCount = 0
        try:
            photoCount = int(articleXML.find("div", "phs").text.strip())
        except:
            pass
        print("photoCount %s" % photoCount)

        # Property Type
        propertyType = \
            articleXML.find_all("div", "col cols5 typeTruncate")[0].text
        print("propertyType %s" % propertyType)

        # Price
        price = \
            int(re.sub("\$|\+|,| |\n", "",
                articleXML.find("strong", "listingPrice").text))
        print("price %s" % price)

        # Bedrooms & Bathrooms
        bedrooms = 0
        bathrooms = 0
        propertySize = 0

        bedRegex = re.compile("(\d+) beds")
        bathRegex = re.compile("(\d+) baths")
        sizeRegex = re.compile("([\d+,]*\d+) sqft")

        articleText = articleXML.text

        bedMatch = bedRegex.search(articleText)
        bathMatch = bathRegex.search(articleText)
        sizeMatch = sizeRegex.search(articleText)

        if bedMatch:
            bedrooms = int(bedMatch.group(1))
        if bathMatch:
            bathrooms = int(bathMatch.group(1))
        if sizeMatch:
            propertySize = int(
                re.sub(",| ", "", sizeMatch.group(1)))
        print("bedrooms %s" % bedrooms)
        print("bathrooms %s" % bathrooms)
        print("propertySize %s" % propertySize)

        # Broker
        broker = None
        try:
            broker = \
                (articleXML.find("p", "typeLowlight typeTruncate mvn")
                    .text
                    .strip())
        except:
            pass
        print("broker %s" % broker)

        return {
            "id": uid,
            "url": url,
            "address": address,
            "latitude": latitude,
            "longitude": longitude,
            "photoCount": photoCount,
            "propertyType": propertyType,
            "price": price,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "propertySize": propertySize,
            "daysOnZillow": 0,
            "broker": broker,
            "zestimate": 0.0
        }

    def parsePage(self, listHTML):
        # Attempt to parse listHTML HTML
        bs = BeautifulSoup(listHTML)
        listings = bs.find_all("li", "propertyCard")
        return [self.extractAttributes(l) for l in listings]


if __name__ == '__main__':
    t = TruliaScraper()
    pages = 61
    properties = []

    for p in xrange(1, (pages + 1)):
        page = t.scrapePage(p)
        parsed = t.parsePage(page)
        properties += parsed
        print parsed

    with open("output/trulia_properties.json", "w+") as f:
        json.dump(properties, f)
