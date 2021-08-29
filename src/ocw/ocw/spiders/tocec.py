import datetime

import scrapy
from ocw.ocw.items import CourseItem

url = "https://www.tocec.org.tw/web/subjects_results.jsp"

class TocecSpider(scrapy.Spider):
    name = 'tocec'
    allowed_domains = ['tocec.org.tw']

    def start_requests(self):
        yield scrapy.Request(url=url, callback=self.parse_main)
    
    def parse_main(self, response):
        # table
        for tr in response.xpath("//tbody//tr"):
            course_item = CourseItem()
            
            course_item["providerInstitution"] = tr.xpath(".//td[1]/text()").get().strip()
            course_item["name"] = tr.xpath(".//td[2]/a/text()").get()
            course_item["url"] = response.urljoin(tr.xpath(".//td[2]/a/@href").get())
            course_item["instructor"] = tr.xpath(".//td[3]/text()").get()
            start_date, end_date = tr.xpath(".//td[4]/text()").get().split("至")
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            course_item["startDate"] = start_date
            course_item["endDate"] = end_date
            course_item["mediaType"] = tr.xpath(".//td[5]/img/@title").extract()
            course_item["source"] = "社團法人台灣開放式課程暨教育聯盟"
            
            yield course_item
                    
        # next page
        if response.xpath("//li/a[@aria-label='Next']/@onclick"):
            next_page = response.xpath("//li[@class='page-item active']/following-sibling::li/a/text()").get()
            yield scrapy.FormRequest.from_response(response=response, formid="form", formdata={"page_num": next_page}, callback=self.parse_main)
    
