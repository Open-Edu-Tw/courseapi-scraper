# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import datetime
from abc import ABC, abstractmethod

import pandas as pd
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from ocw.items import TypedCourseItem


class PipelineAbstract(ABC):
    @abstractmethod
    def open_spider(self, spider): pass

    @abstractmethod
    def process_item(self, item: TypedCourseItem, spider) -> TypedCourseItem: pass

    @abstractmethod
    def close_spider(self, spider): pass


class CourseItemCheckPipeline(PipelineAbstract):
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item: TypedCourseItem, spider) -> TypedCourseItem:
        return item


class SaveToCsvPipeline(PipelineAbstract):
    items: list[dict] = None

    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider) -> TypedCourseItem:
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
    db_client: MongoClient = None
    db: Database = None

    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', 'mongodb://localhost:27017')
        db_name = spider.settings.get('MONGODB_DB_NAME', 'scraping')
        self.db_client = MongoClient(db_uri)
        self.db = self.db_client[db_name]

    def process_item(self, item: TypedCourseItem, spider) -> TypedCourseItem:
        # filter only needed
        insert_dict = {
            "name": item.name,
            "url": item.url,
            "instructor": item.instructor,
            "description": item.description,
            "providerInstitution": item.provider_institution,
            "source": item.source
        }
        self.insert_course(insert_dict)
        return item

    def insert_course(self, item: dict):
        course: Collection = self.db.course
        course.insert_one(item)

    def close_spider(self, spider):
        self.db_client.close()
