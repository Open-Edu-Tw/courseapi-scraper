import datetime

import scrapy
from scrapy.http import HtmlResponse
from ocw.items import CourseItem
from ocw.spiders.Scraper import OCWScraper, init_logger

url = "https://www.openedu.tw/list.jsp"


class OpenEduSpider(OCWScraper):
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
        course_item = CourseItem()
        course_item["name"] = course_dict.get("name", None)
        course_item["url"] = response.url
        course_item["providerInstitution"] = course_dict.get("institute", None)
        course_item["startDate"] = self.get_date(course_dict, "startDate")
        course_item["endDate"] = self.get_date(course_dict, "endDate")
        course_item["certification"] = course_dict.get("certificate", None)  # bool
        course_item["category"] = course_dict.get("category", None)
        course_item["lectureLanguage"] = course_dict.get("language", None)
        course_item["price"] = course_dict.get("price", None)
        course_item["description"] = course_dict.get("intro", None)  # html text
        course_item["objective"] = course_dict.get("objective", None)   # html text
        course_item["TA"] = course_dict.get("target", "")  # html text
        course_item["schedule"] = course_dict.get("schedule", None)
        course_item["evaluation"] = course_dict.get("assessment", None)
        course_item["subtitleLanguage"] = course_dict.get("transcript", None)
        course_item["instructor"] = [instructor["name"] for instructor in course_dict["instructors"]]
        course_item["hoursPerWeek"] = course_dict.get("hoursPerWeek", None)
        course_item["videoUrl"] = course_dict.get("videoUrl", None)
        course_item["prerequisites"] = course_dict.get("prerequisite", None)
        course_item["source"] = "中華開放教育平台"

        yield course_item

    def get_value(self, course_dict, key):
        return course_dict[key]

    def get_date(self, course_dict, key):
        if key in course_dict and course_dict[key]:
            return datetime.datetime.strptime(course_dict["startDate"], "%Y-%m-%d")
        return None
