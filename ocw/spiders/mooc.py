import scrapy

from ocw.items import CourseItem
from ocw.spiders.Scraper import OCWScraper

url = "https://taiwanmooc.org/listing/ajaxfilter_pagelink"


class MoocSpider(OCWScraper):
    name = "mooc"
    allowed_domains = ["taiwanmooc.org"]

    def start_requests(self):
        yield scrapy.Request(url=url, callback=self.parse_course_directoy)

    def parse_course_directoy(self, response):
        courses = response.xpath("//div[@class='course-box']")
        for course in courses:
            course_url = course.xpath(".//a/@href").get()
            yield scrapy.Request(url=course_url, callback=self.parse_course)

        # next page
        if "page" not in response.meta:  # run only at first page
            last_page_num = int(
                response.xpath(
                    "//a[@data-ci-pagination-page and contains(text(), 'Last')]/@data-ci-pagination-page"
                ).get()
            )
            for p in range(1, last_page_num + 1):
                yield scrapy.Request(
                    f"{url}/{len(courses) * p}",
                    callback=self.parse_course_directoy,
                    meta={"page": p},
                )

    def parse_course(self, response):
        course_item = CourseItem(
            name=response.xpath("//h1/text()").get(),
            url=response.url,
            instructor=response.xpath(
                "//div[@class='teacher-box']//*[self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6 or self::h7 or self::h8]/text()"
            ).extract(),
            provider_institution=response.xpath(
                "//*[contains(text(), 'Institution')]/following-sibling::a/text()"
            ).get(),
            description=self._get_description(response),
            source="磨課師",
        )
        yield course_item

    @staticmethod
    @OCWScraper.get_element_handler(default_return_value="")
    def _get_description(response) -> str:
        texts = response.xpath(
            "//div[@id='cs-desc']/div[@class='content-box']/descendant-or-self::*/text()"
        ).extract()
        description = " ".join(texts).strip().replace("\n", " ")
        return description
