from abc import ABC

import scrapy
from ocw.items import CourseItem
from ocw.spiders.Scraper import OCWScraper

url = "https://www.sharecourse.net/sharecourse/course/view/categorySearch/6/23?type=2&page=1"


class ShardCourseSpider(OCWScraper, ABC):
    name = 'sharecourse'
    allowed_domains = ['sharecourse.net']

    def start_requests(self):
        yield scrapy.Request(url=url, callback=self.parse_main)

    def parse_main(self, response):
        courses = response.xpath("//div[@class='item']")
        for course in courses:
            course_url = course.xpath(".//a/@href").get()
            teacher = course.xpath(".//p[@class='teacher']/text()").get().strip()
            yield scrapy.Request(url=course_url,
                                 callback=self.parse_course,
                                 cb_kwargs={"teacher": teacher})

        # next page
        if "page" not in response.meta:  # run only at first page
            last_page_num = int(
                response.xpath("//ul[@class='pagination']/li/a/@href").extract()[-1].split("&page=")[-1])
            for p in range(2, last_page_num + 1):
                yield scrapy.Request("https://www.sharecourse.net/sharecourse/course/view/categorySearch/6/23"
                                     f"?type=2&page={p}", callback=self.parse_main, meta={"page": p})

    def parse_course(self, response, teacher: str):
        yield CourseItem(
            name=response.xpath("//h1/text()").get(),
            url=response.url,
            instructor=[teacher],
            provider_institution="ShareCourse",
            description=self._get_description(response),
            source="ShareCourse 學聯網"
        )

    @staticmethod
    @OCWScraper.get_element_handler(default_return_value="")
    def _get_description(response) -> str:
        texts = response.xpath("//div[@id='cs-desc']/div[@class='content-box']/descendant-or-self::*/text()").extract()
        description = " ".join(texts).strip().replace("\n", " ")
        return description
