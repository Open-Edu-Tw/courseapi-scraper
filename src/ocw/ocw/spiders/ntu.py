import datetime

import scrapy
from ocw.items import CourseItem
from ocw.spiders.Scraper import OCWScraper

url = "http://ocw.aca.ntu.edu.tw/ntu-ocw/ocw/coupage"


class NtuSpider(OCWScraper):
    name = 'ntu'
    allowed_domains = ['ocw.aca.ntu.edu.tw']

    def start_requests(self):
        yield scrapy.Request(url=url, callback=self.parse_main)

    def parse_main(self, response):
        courses = response.xpath("//div[@class='coursebox']")
        for course in courses:
            course_url = course.xpath(".//a/@href").get()
            teacher = course.xpath(".//div[@class='teacher']/text()").get().strip()
            yield scrapy.Request(url=course_url,
                                 callback=self.parse_course,
                                 meta={"teacher": teacher})

        # next page
        if "page" not in response.meta:  # run only at first page
            last_page_num = int(response.xpath("//a[@title='最後一頁']/@href").get().split("/")[-1])
            for p in range(2, last_page_num + 1):
                yield scrapy.Request(f"{response.url}/{p}", callback=self.parse_main, meta={"page": p})

    def parse_course(self, response):
        course_item = CourseItem()
        course_item["name"] = response.xpath("//h2[@class='title']/text()").get()
        course_item["url"] = response.url
        course_item["instructor"] = response.meta["teacher"]
        course_item["providerInstitution"] = "NTU"
        course_item["providerDepartment"] = self.get_department(response)
        course_item["description"] = self.get_description(response)
        course_item["mediaType"] = self.get_media_type(response)
        course_item["source"] = "國立臺灣大學"

        yield course_item

    @OCWScraper.get_element_handler(default_return_value=None)
    def get_department(self, response):
        department = response.xpath("//h4[@class='unit']/text()").get().split(" ")[0].split("\xa0")[0]
        if department:
            return department
        return None

    @OCWScraper.get_element_handler(default_return_value="")
    def get_description(self, response):
        return response.xpath("//h4[@class='unit']/following-sibling::p/text()").get().strip()

    @OCWScraper.get_element_handler(default_return_value="")
    def get_start_end_date(self, tr):
        start_date, end_date = tr.xpath(".//td[4]/text()").get().split("至")
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        return start_date, end_date

    @OCWScraper.get_element_handler(default_return_value=[])
    def get_media_type(self, response):
        is_video = len(response.xpath("//img[contains(@src, 'icon-V')]")) > 0
        is_slide = len(response.xpath("//img[contains(@src, 'icon-L')]")) > 0
        medias = []
        if is_video:
            medias.append("Video")
        if is_slide:
            medias.append("Slide")
        return medias
