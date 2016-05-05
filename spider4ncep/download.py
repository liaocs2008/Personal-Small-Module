# tutorial
# http://doc.scrapy.org/en/latest/topics/media-pipeline.html
# http://doc.scrapy.org/en/latest/intro/tutorial.html

import os
import scrapy

class NCEPItem(scrapy.Item):
    save_path = scrapy.Field()
    file_urls = scrapy.Field()

class NCEPSpider(scrapy.Spider):
    name = "ncep"
    allowed_domains = ["noaa.gov"]
    start_urls = [
        "http://mrms.ncep.noaa.gov/data/2D/PrecipRate/",
    ]

    def parse(self, response):
        for href in response.xpath("//tr/td/a/@href"):
            filename = href.extract()
            if "grib2" not in filename:
                continue
            else:
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.save_file)

    def save_file(self, response):
        url = response.url

        # create dir by date
        path = url.replace('-', '_').split('_')[-2]
        if not os.path.exists(path):
            os.makedirs(path)

        # save file to the dir
        filename = path + "/" + url.split('/')[-1]
        if not os.path.isfile(filename):
            with open(filename, "wb") as f:
                f.write(response.body)
            print "finishing writing", filename
        else:
            print "found existing", filename