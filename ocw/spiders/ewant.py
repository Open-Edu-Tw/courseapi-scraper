from abc import ABC
from urllib.parse import parse_qsl, urlencode, urlparse

import scrapy  # type: ignore

from ocw.items import CourseItem
from ocw.spiders.Scraper import OCWScraper

url = "https://www.ewant.org/admin/tool/mooccourse/allcourses.php?lang=zh_tw"


class EwantScraper(OCWScraper, ABC):
    name = "ewant"
    allowed_domains = ["ewant.org"]

    def start_requests(self):
        yield scrapy.Request(url=url, callback=self.parse_course_list)

    def parse_course_list(self, response):
        # iterate all school_ids -> iterate all pages
        query = dict(parse_qsl(urlparse(response.url).query))

        # (first) iterate school_ids
        if "schoolid" not in query:
            schools = response.xpath(
                "//select[(@id='menuschoolid')]//option[not(@value='0')]"
            )
            school_id_dict = {}
            for school in schools:
                value = school.xpath("./@value").get()
                school_name = school.xpath("./text()").get()
                school_id_dict[value] = school_name

            for school_id, school_name in school_id_dict.items():
                yield scrapy.Request(
                    url=response.urljoin("?" + urlencode({"schoolid": school_id})),
                    callback=self.parse_course_list,
                    meta={"school_name": school_name},
                )
        else:
            # (last) iterate all courses in one page
            courses = response.xpath("//div[@class='course-info-item']")
            for course in courses:
                course_url = course.xpath("./div[@class='courseimage']/a/@href").get()
                yield scrapy.Request(
                    url=course_url + "?lang=zh_tw",
                    callback=self.parse_course,
                    cb_kwargs={"provider_institution": response.meta["school_name"]},
                )
            # (second) iterate all pages from one school_id
            if "p" not in query:
                pages = [
                    page.strip()
                    for page in response.xpath(
                        "//ul[contains(@class, 'pagination')]//li/a/text()"
                    ).extract()
                ]
                if pages:
                    last_page_num = max([int(page) for page in pages if page])
                    last_page_num = 1
                    for p in range(1, int(last_page_num)):
                        query[p] = p
                        yield scrapy.Request(
                            response.urljoin("?" + urlencode(query)),
                            callback=self.parse_course_list,
                            meta=response.meta,
                        )

    def parse_course(self, response, provider_institution):
        yield CourseItem(
            name=response.xpath("//div[@class='coursename']/text()").get(),
            description=" ".join(
                response.xpath(
                    "//h3[contains(text(), '摘要')]/following-sibling::div/descendant-or-self::*/text()"
                ).extract()
            ),
            instructor=self._get_instructors(response),  # messy
            url=response.url,
            source="育網開放教育平台",
            provider_institution=provider_institution,
        )

    @staticmethod
    def _get_school_id(url):
        query = urlparse(url).query
        school_id = query["hostid"]
        return school_id

    @staticmethod
    def _get_instructors(response):
        teachers = response.xpath("//div[@class='teachername']/text()").get()
        if teachers:
            teachers = teachers.replace("教師: ", "").split(",")
        else:
            teachers = [""]
        return teachers
