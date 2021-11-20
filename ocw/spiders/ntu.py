from abc import ABC
from typing import List

import scrapy

from ocw.spiders.Scraper import OCWScraper

from ocw.items import TypedCourseItem, MediaType

url = "http://ocw.aca.ntu.edu.tw/ntu-ocw/ocw/coupage"


class NtuSpider(OCWScraper, ABC):
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
        yield TypedCourseItem(
            name=response.xpath("//h2[@class='title']/text()").get(),
            url=response.url,
            instructor=[response.meta["teacher"]],
            provider_institution="NTU",
            provider_department=self._get_department(response),
            description=self._get_description(response),
            media_type=self._get_media_type(response),
            source="國立臺灣大學",
        )

    @OCWScraper.get_element_handler(default_return_value=None)
    def _get_department(self, response) -> str:
        department = response.xpath("//h4[@class='unit']/text()").get().split(" ")[0].split("\xa0")[0]
        return department

    @classmethod
    @OCWScraper.get_element_handler(default_return_value="")
    def _get_description(cls, response) -> str:
        return response.xpath("//h4[@class='unit']/following-sibling::p/text()").get().strip()

    @classmethod
    @OCWScraper.get_element_handler(default_return_value=[])
    def _get_media_type(cls, response) -> List[MediaType]:
        def is_xpath(xpath):
            return len(response.xpath(xpath)) > 0

        medias: List[MediaType] = []

        is_video = is_xpath("//img[contains(@src, 'icon-V')]")
        is_slide = is_xpath("//img[contains(@src, 'icon-L')]")

        if is_video:
            medias.append(MediaType.VIDEO)

        if is_slide:
            medias.append(MediaType.SLIDE)

        return medias
