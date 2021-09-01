import datetime

import scrapy
from ocw.items import CourseItem
from ocw.spiders.Scraper import OCWScraper

url = "https://www.tocec.org.tw/web/subjects_results.jsp"

class TocecSpider(OCWScraper):
    name = 'tocec'
    allowed_domains = ['tocec.org.tw']
    defined_columns = ["providerInstitution", "name", "url", "instructor", "startDate", "endDate", "mediaType", "source"]

    def start_requests(self):
        yield scrapy.Request(url=url, callback=self.parse_main)
        
    def parse_main(self, response):
        # table
        for tr in response.xpath("//tbody//tr"):
            course_item = CourseItem()
            
            course_item["providerInstitution"] = self.get_institution(tr)
            course_item["name"] = self.get_course_name(tr)
            course_item["url"] = response.urljoin(self.get_course_href(tr))
            course_item["instructor"] = self.get_instructor(tr)
            start_date, end_date = self.get_start_end_date(tr)
            course_item["startDate"] = start_date
            course_item["endDate"] = end_date
            course_item["mediaType"] = self.get_media_type(tr)
            course_item["source"] = "社團法人台灣開放式課程暨教育聯盟"
            
            yield course_item
                    
        # next page
        if response.xpath("//li/a[@aria-label='Next']/@onclick"):
            next_page = response.xpath("//li[@class='page-item active']/following-sibling::li/a/text()").get()
            yield scrapy.FormRequest.from_response(response=response, formid="form", formdata={"page_num": next_page}, callback=self.parse_main)

    @OCWScraper.get_element_handler(default_return_value="")
    def get_institution(self, tr):
        return tr.xpath(".//td[1]/text()").get().strip()
    
    @OCWScraper.get_element_handler(default_return_value="")
    def get_course_name(self, tr):
        return tr.xpath(".//td[2]/a/text()").get()
    
    @OCWScraper.get_element_handler(default_return_value="")
    def get_course_href(self, tr):
        return tr.xpath(".//td[2]/a/@href").get()
    
    @OCWScraper.get_element_handler(default_return_value="")
    def get_instructor(self, tr):
        return tr.xpath(".//td[3]/text()").get()
    
    @OCWScraper.get_element_handler(default_return_value="")
    def get_start_end_date(self, tr):
        start_date, end_date = tr.xpath(".//td[4]/text()").get().split("至")
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        return start_date, end_date
    
    @OCWScraper.get_element_handler(default_return_value="")
    def get_media_type(self, tr):
        return tr.xpath(".//td[5]/img/@title").extract()