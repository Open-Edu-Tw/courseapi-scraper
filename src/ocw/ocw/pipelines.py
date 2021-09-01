# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import datetime

import pandas as pd
from scrapy.exceptions import DropItem


class CourseItemCheckPipeline:
    def process_item(self, item, spider):
        # type check
        for colname in ["startDate", "endDate"]:
            if colname in item and item[colname] and not isinstance(item[colname], datetime.datetime):
                spider.logger.error(f"[Type Error] {colname} in course {item['name']} is not datetime.")
        
        # mandatory column
        for colname in spider.mandatory_columns:
            if not item[colname]:
                raise DropItem(f"[Empty Result] {colname} in course {item['name']} is empty.")
            
        return item

class SaveToCsvPipeline:
    file = None
    def open_spider(self, spider):
        self.items = []
    
    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item
    
    def close_spider(self, spider):
        save_path = os.path.join(spider.settings["FILES_STORE"], spider.name, f"{datetime.datetime.now().strftime('%Y-%m-%d')}.csv")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        df = pd.DataFrame(self.items)
        df[spider.defined_columns].to_csv(save_path)
        spider.logger.info(f"Csv is exported to {save_path}. Total records={len(df)}")

        