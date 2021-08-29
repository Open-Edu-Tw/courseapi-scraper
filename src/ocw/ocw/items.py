# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseItem(scrapy.Item):
    url = scrapy.Field()
    mode = scrapy.Field()
    name = scrapy.Field()
    englishName = scrapy.Field()
    providerInstitution = scrapy.Field()
    providerDepartment = scrapy.Field()
    instructor = scrapy.Field()
    establishDate = scrapy.Field()
    hitCount = scrapy.Field()
    category = scrapy.Field()
    lectureLanguage = scrapy.Field()
    subtitleLanguage = scrapy.Field()
    price = scrapy.Field()
    TA = scrapy.Field()
    highlight = scrapy.Field()
    schedule = scrapy.Field()
    subcategory = scrapy.Field()
    isSelfLearning = scrapy.Field()
    description = scrapy.Field()
    startDate = scrapy.Field()
    endDate = scrapy.Field()
    evaluation = scrapy.Field()
    prerequisites = scrapy.Field()
    others = scrapy.Field()
    HoursPerWeek = scrapy.Field()
    introductionVideoUrl = scrapy.Field()
    deadline = scrapy.Field()
    updatedDate = scrapy.Field()
    teachingMethod = scrapy.Field()
    extendedCourse = scrapy.Field()
    content = scrapy.Field()
    pass_standard = scrapy.Field()
    certification = scrapy.Field()
    media_type = scrapy.Field()
    school_semester = scrapy.Field()
    media_count = scrapy.Field()
    references = scrapy.Field()
    