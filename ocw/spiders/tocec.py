import datetime
from abc import ABC

import scrapy
from ocw.items import CourseItem, MediaType
from ocw.spiders.Scraper import OCWScraper

url = "https://www.tocec.org.tw/web/subjects_results.jsp"


class TocecSpider(OCWScraper, ABC):
    name = 'tocec'
    allowed_domains = ['tocec.org.tw']

    def start_requests(self):
        yield scrapy.Request(url=url, callback=self.parse_main)

    def parse_main(self, response):
        # table
        for tr in response.xpath("//tbody//tr"):
            start_date, end_date = self._get_start_end_date(tr)
            name, relative_url = self._get_course_name_and_href(tr)
            course_url = response.urljoin(relative_url)
            course_item = CourseItem(
                provider_institution=self._get_institution(tr),
                name=name,
                url=course_url,
                instructor=[self._get_instructor(tr)],
                start_date=start_date,
                end_date=end_date,
                media_type=self._get_media_type(tr),
                source="社團法人台灣開放式課程暨教育聯盟",
                description="",  # will be written in parse_description()
            )

            yield scrapy.Request(
                url=course_url,
                callback=self.parse_description,
                cb_kwargs={"item": course_item}
            )

        # next page
        if response.xpath("//li/a[@aria-label='Next']/@onclick"):
            next_page = response.xpath("//li[@class='page-item active']/following-sibling::li/a/text()").get()
            yield scrapy.FormRequest.from_response(
                response=response,
                formid="form",
                formdata={"page_num": next_page},
                callback=self.parse_main
            )

    @classmethod
    def parse_description(cls, response, item: CourseItem):
        description = response.css("div.ClassInfo").get()
        item.description = description
        yield item

    @OCWScraper.get_element_handler(default_return_value="")
    def _get_institution(self, tr) -> str:
        return tr.xpath(".//td[1]/text()").get().strip()

    @OCWScraper.get_element_handler(default_return_value="")
    def _get_course_name_and_href(self, tr) -> (str, str):
        course = tr.xpath(".//td[2]/a") #/text()").get()
        name = course.xpath("./text()").get()
        href = course.xpath("./@href").get()

        return name, href

    @OCWScraper.get_element_handler(default_return_value="")
    def _get_instructor(self, tr) -> str:
        return tr.xpath(".//td[3]/text()").get()

    @OCWScraper.get_element_handler(default_return_value="")
    def _get_start_end_date(self, tr) -> (datetime, datetime):
        start_date, end_date = tr.xpath(".//td[4]/text()").get().split("至")
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        return start_date, end_date

    @OCWScraper.get_element_handler(default_return_value="")
    def _get_media_type(self, tr) -> list[MediaType]:
        media_type: list[MediaType] = []
        v = tr.xpath(".//td[5]/img/@title").extract()

        # As we don't pretty sure what the type of `v`
        # is, we parse `v` to a new explicit array to
        # prevent the type issue.
        for raw_type in v:
            match raw_type:
                case "Media":
                    media_type.append(MediaType.VIDEO)
                case "Paper":
                    media_type.append(MediaType.PAPER)
                case _:
                    media_type.append(MediaType.UNKNOWN)

        return media_type
