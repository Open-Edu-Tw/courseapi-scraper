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
    hoursPerWeek = scrapy.Field()
    videoUrl = scrapy.Field()
    deadline = scrapy.Field()
    updatedDate = scrapy.Field()
    teachingMethod = scrapy.Field()
    extendedCourse = scrapy.Field()
    content = scrapy.Field()
    passStandard = scrapy.Field()
    certification = scrapy.Field()
    certificationFee = scrapy.Field()
    mediaType = scrapy.Field()
    schoolSemester = scrapy.Field()
    mediaCount = scrapy.Field()
    references = scrapy.Field()
    objective = scrapy.Field()
    source = scrapy.Field()
    
    def __repr__(self):
        return f"{self['name']}({self['url']})"