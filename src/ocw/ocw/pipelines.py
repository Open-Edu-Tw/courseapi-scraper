# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import datetime
from abc import ABC, abstractmethod

import pandas as pd
from pymongo import MongoClient

from scrapy.exceptions import DropItem


class PipelineAbstract(ABC):
    @abstractmethod
    def open_spider(self, spider): pass

    @abstractmethod
    def process_item(self, item, spider): pass

    @abstractmethod
    def close_spider(self, spider): pass


def date_check(item, spider):
    for column_name in ["startDate", "endDate"]:
        if column_name in item and item[column_name] and not isinstance(item[column_name], datetime.datetime):
            spider.logger.error(f"[Type Error] {column_name} in course {item['name']} is not datetime.")


class CourseItemCheckPipeline(PipelineAbstract):
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # type check
        date_check(item, spider)

        # mandatory column
        for colname in spider.mandatory_columns:
            if not item[colname]:
                raise DropItem(f"[Empty Result] {colname} in course {item['name']} is empty.")

        return item


class SaveToCsvPipeline(PipelineAbstract):
    file = None
    items = None

    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        save_path = os.path.join(spider.settings["FILES_STORE"], spider.name,
                                 f"{datetime.datetime.now().strftime('%Y-%m-%d')}.csv")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        df = pd.DataFrame(self.items)
        df.to_csv(save_path)
        spider.logger.info(f"CSV has been exported to {save_path}. Total records={len(df)}")


class MongoDBPipeline(PipelineAbstract):
    db_client = None
    db = None

    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', 'mongodb://localhost:27017')
        db_name = spider.settings.get('MONGODB_DB_NAME', 'scraping')
        self.db_client = MongoClient(db_uri)
        self.db = self.db_client[db_name]

    def process_item(self, item, spider):
        # filter only needed
        course_dict = dict(item)
        insert_dict = {}
        for key in ["name", "url", "instructor", "description", "providerInstitution", "source"]:
            if key in course_dict:
                insert_dict[key] = course_dict[key]
            else:
                insert_dict[key] = ""
        self.insert_course(insert_dict)
        return item

    def insert_course(self, item: dict):
        self.db.course.insert_one(item)

    def close_spider(self, spider):
        self.db_client.close()
