import datetime
from abc import ABC

import scrapy
from ocw.items import CourseItem
from ocw.spiders.Scraper import OCWScraper

url = "https://www.openedu.tw/list.jsp"


class OpenEduSpider(OCWScraper, ABC):
    name = 'openedu'
    allowed_domains = ['openedu.tw']

    def start_requests(self):
        yield scrapy.Request(url="https://www.openedu.tw/api/courses/search?lang=en", callback=self.parse_main)

    def parse_main(self, response):
        courses = response.json()
        for course in courses:
            yield scrapy.Request(url=f"https://www.openedu.tw/api/courses/{course['id']}/lang/zh",
                                 callback=self.parse_course)

    def parse_course(self, response):
        course_dict = response.json()

        yield CourseItem(
            name=course_dict.get("name", ""),
            url=response.url,
            provider_institution=course_dict.get("institute", None),
            start_date=self._get_date(course_dict, "startDate"),
            end_date=self._get_date(course_dict, "endDate"),
            certification=course_dict.get("certificate", False),
            category=[course_dict.get("category", "")],
            lecture_language=course_dict.get("language", None),
            price=course_dict.get("price", None),
            description=course_dict.get("intro", ""),
            objective=course_dict.get("objective", None),
            TA=course_dict.get("target", None),
            schedule=course_dict.get("schedule", None),
            evaluation=course_dict.get("assessment", None),
            subtitle_language=[course_dict.get("category", "")],
            instructor=[instructor["name"] for instructor in course_dict["instructors"]],
            hours_per_week=course_dict.get("hoursPerWeek", None),
            video_url=course_dict.get("videoUrl", None),
            prerequisites=course_dict.get("prerequisite", None),
            source="中華開放教育平台"
        )

    @staticmethod
    @OCWScraper.get_element_handler(default_return_value=None)
    def _get_date(course_dict, key) -> datetime.datetime | None:
        if key in course_dict and course_dict[key]:
            return datetime.datetime.strptime(course_dict[key], "%Y-%m-%d")
        return None
