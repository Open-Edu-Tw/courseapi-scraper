# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import datetime

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CourseItemPipeline:
    def process_item(self, item, spider):
        # type check
        for colname in ["startDate", "endDate"]:
            if item[colname] and not isinstance(item[colname], datetime.datetime):
                spider.logger.error(f"[TypeError] {colname} in course is not datetime")
        return item
