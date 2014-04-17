from bs4 import BeautifulSoup

import json
import re

import urllib
import urllib2

# Zillow search URL
BASE_ZILLOW_SEARCH_URL = "http://www.zillow.com/search/GetResults.htm"


class ZillowScraper(object):
    def requestParams(self, page):
        return \
            {
                "status": 100000,
                "lt": 11110,
                "ht": 11111,
                "bd": 0,
                "ba": 0,
                "pho": 0,
                "pets": 0,
                "parking": 0,
                "laundry": 0,
                "pnd": 0,
                "red": 0,
                "zso": 0,
                "days": any,
                "ds": all,
                "pmf": 0,
                "pf": 0,
                "zoom": 11,
                "rect": "-122525368,37672000,-122300491,37835412",
                "p": page,
                "sort": "days",
                "search": "list",
                "disp": 1,
                "rid": 20330,
                "rt": 6,
                "listright": "true",
                "responsivemode": "defaultList",
                "isMapSearch": "false",
                "zoom": 11
            }

    def scrapePage(self, pageNum):
        # URL Params
        encodedRequestParamsStr = self.requestParams(pageNum)
        getURL = BASE_ZILLOW_SEARCH_URL \
            + "?" \
            + urllib.urlencode(encodedRequestParamsStr)

        # Run the request
        return urllib2.urlopen(getURL).read()

    def extractAttributes(self, articleXML):
        """
         Spit out attributes as dictionary:

         Unique ID
         URL
         Address
         Latitude, Longitude
         Photo Count
         Property Type
         Price
         # Bedrooms
         # Bathrooms
         Property Size (sqft)
         Property Year
         Days on Zillow
         Broker
         Zestimate

        """
        # Extract Zillow ID
        uid = articleXML["id"]
        print "uid", uid

        # Extract URL
        propertyLink = articleXML.find("dt", "property-address").find("a")
        url = "www.zillow.com" + propertyLink["href"]
        print "url", url

        # Address
        address = propertyLink.text
        print "address", address

        # Lat/Long
        latitude = articleXML["latitude"]
        longitude = articleXML["longitude"]
        print "lat, long", latitude, longitude

        # Photo Count
        photoCount = 0
        try:
            photoCount = int(
                articleXML.find("figcaption", "photo-count").text.split()[0])
        except:
            pass
        print "photos", photoCount

        # Property Type
        propertyType = None
        try:
            articleXML.find("dt", "type-forSale").text.split()[0]
        except:
            pass
        print "properties", propertyType

        # Extract Price
        price = None
        try:
            price = \
                int(re.sub("\$|,| ", "",
                    articleXML.find("dt", "price-large").text))
        except:
            pass
        print "price", price

        # Bedrooms, Bathrooms, Property Size
        propertyTag = articleXML.find("dt", "property-data")
        bedrooms = 0.0    # assume no bedrooms by default
        bathrooms = 1.0   # assume one bathroom by default
        propertySize = None

        if propertyTag:
            propertyText = propertyTag.text
            if "Studio" not in propertyText:
                bedRegex = re.compile("(\d+) beds")
                bathRegex = re.compile("(\d+\.\d+) bath")
                sizeRegex = re.compile("([\d+,]*\d+) sqft")

                bedMatch = bedRegex.search(propertyText)
                bathMatch = bathRegex.search(propertyText)
                sizeMatch = sizeRegex.search(propertyText)

                if bedMatch:
                    bedrooms = float(bedMatch.group(1))
                if bathMatch:
                    bathrooms = float(bathMatch.group(1))
                if sizeMatch:
                    propertySize = int(
                        re.sub("\$|,| ", "", sizeMatch.group(1)))
            print "bed, bath, size", bedrooms, bathrooms, propertySize

        # Property Year
        yearRegex = re.compile("\d+")
        propertyYear = None
        yearTag = articleXML.find("dt", "property-year")
        if yearTag:
            propertyYearMatch = yearRegex.search(yearTag.text)
            if propertyYearMatch:
                propertyYear = int(propertyYearMatch.group(0))
        print "year", propertyYear

        # Days on Zillow
        daysOnZillow = None
        daysOnZillowTag = articleXML.find("dt", "doz")
        if daysOnZillowTag:
            daysOnZillow = int(daysOnZillowTag
                               .find("span", "sorted-attribute")
                               .text)
        print "daysOnZillow", daysOnZillow

        # Broker
        broker = None
        brokerTag = articleXML.find("dt", "property-broker")
        if brokerTag:
            broker = brokerTag["title"]
        print "broker", broker

        # Zestimate
        zestimate = None
        zestimateTag = articleXML.find("div", "zestimate")
        if zestimateTag:
            zestimateRegex = re.compile("(\d+.?\d+)(M|K)")
            zestimateMatch = zestimateRegex.search(zestimateTag.text)
            if zestimateMatch:
                zestimateText = zestimateMatch.group(0)
                if "M" in zestimateText:
                    zestimate = \
                        float(re.sub("\$|,| |M|K", "", zestimateText)) * 10**6
                elif "K" in zestimateText:
                    zestimate = \
                        float(re.sub("\$|,| |M|K", "", zestimateText)) * 10**3
        print "zestimate", zestimate

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
            "daysOnZillow": daysOnZillow,
            "broker": broker,
            "zestimate": zestimate
        }

    def parsePage(self, pageObject):
        # Attempt to parse JSON Object
        jsonObject = json.loads(pageObject)
        listHTML = jsonObject['list']['listHTML']

        # Attempt to parse listHTML HTML
        bs = BeautifulSoup(listHTML)
        articles = bs.find_all("article")
        return [self.extractAttributes(a) for a in articles]


if __name__ == '__main__':
    z = ZillowScraper()
    pages = 24
    properties = []

    for p in xrange(1, (pages + 1)):
        page = z.scrapePage(p)
        properties += z.parsePage(page)

    with open("output/zillow_properties.json", "w") as f:
        json.dump(properties, f)
