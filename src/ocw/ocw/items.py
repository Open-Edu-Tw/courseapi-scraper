# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime
from enum import Enum
from typing import Optional, Any, List, Dict

import scrapy
from pydantic import BaseModel

# 選擇性填寫的文字。
o_str = Optional[str]
# 選擇性填寫的數字。
o_int = Optional[int]
# 選擇性填寫的 datetime
o_datetime = Optional[datetime]


class MediaType(Enum):
    VIDEO = "video"
    SLIDE = "slide"


class TypedCourseItem(BaseModel):
    """一個課程的各個資訊。"""
    # 課程的 URL
    url: str
    # 課程名稱
    name: str
    # 描述文字
    description: str
    # 提供者隸屬的機構
    provider_institution: str
    # 指導者
    instructor: str
    # 來源
    source: str
    # ??
    mode: Any
    # 課程英文名稱
    english_name: o_str
    # 提供者隸屬的部門
    provider_department: o_str
    # 建立時間
    establish_date: o_str
    # 點閱率
    hit_count: o_int
    # 分類
    category: List[str]
    # 教授語言
    lecture_language: o_str
    # 字幕語言
    subtitle_language: List[str]
    # 課程價格
    price: str
    # ?
    TA: Any
    # 凸顯部分?
    highlight: Any
    # 排程？
    schedule: Any
    # 子分類
    subcategory: List[str]
    # 是否為自主學習
    is_self_learning: bool
    # 起始日期
    start_date: o_datetime
    # 結束日期
    end_date: o_datetime
    # 評估?
    evaluation: Any
    # 課前要求
    prerequisites: o_str
    # 其他部分
    others: Dict[str, str]
    # 每週時數
    hours_per_week: int
    # 影片 URL
    video_url: o_str
    # 截止日期
    deadline: o_datetime
    # 更新日期
    updated_date: o_datetime
    # 教學方式
    teaching_method: o_str
    # 延伸課程
    extended_course: List[str]
    # 內容
    content: o_str
    # ?
    pass_standard: o_str
    # 證照
    certification: o_str
    # 證照費用
    certification_fee: o_str
    # 媒體類型
    media_type: List[MediaType]
    # 學校學期 [-> ?]
    school_semester: o_str
    # 媒體數？
    media_count: int
    # 參考
    references: o_str
    # 主體
    objective: o_str


class CourseItem(scrapy.Item):
    url = scrapy.Field()
    mode = scrapy.Field()
    name = scrapy.Field()
    english_name = scrapy.Field()
    provider_institution = scrapy.Field()
    provider_department = scrapy.Field()
    instructor = scrapy.Field()
    establish_date = scrapy.Field()
    hit_count = scrapy.Field()
    category = scrapy.Field()
    lecture_language = scrapy.Field()
    subtitle_language = scrapy.Field()
    price = scrapy.Field()
    TA = scrapy.Field()
    highlight = scrapy.Field()
    schedule = scrapy.Field()
    subcategory = scrapy.Field()
    is_self_learning = scrapy.Field()
    description = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    evaluation = scrapy.Field()
    prerequisites = scrapy.Field()
    others = scrapy.Field()
    hours_per_week = scrapy.Field()
    video_url = scrapy.Field()
    deadline = scrapy.Field()
    updated_date = scrapy.Field()
    teaching_method = scrapy.Field()
    extended_course = scrapy.Field()
    content = scrapy.Field()
    pass_standard = scrapy.Field()
    certification = scrapy.Field()
    certification_fee = scrapy.Field()
    media_type = scrapy.Field()
    school_semester = scrapy.Field()
    media_count = scrapy.Field()
    references = scrapy.Field()
    objective = scrapy.Field()
    source = scrapy.Field()

    def __repr__(self):
        return f"{self['name']}({self['url']})"
