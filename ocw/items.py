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
# 選擇性填寫的 datetime。
o_datetime = Optional[datetime]
# 選擇性填寫的 boolean。
o_bool = Optional[bool]


class MediaType(Enum):
    VIDEO = "video"
    SLIDE = "slide"
    PAPER = "paper"
    UNKNOWN = "unknown"


class TypedCourseItem(BaseModel):
    """一個課程的各個資訊。"""
    # 課程的 URL
    url: str
    # 課程名稱
    name: str
    # 描述文字 (html text)
    description: str
    # 提供者隸屬的機構
    provider_institution: str
    # 指導者
    instructor: List[str]
    # 來源
    source: str
    # ??
    mode: Any = None
    # 課程英文名稱
    english_name: o_str = None
    # 提供者隸屬的部門
    provider_department: o_str = None
    # 建立時間
    establish_date: o_str = None
    # 點閱率
    hit_count: o_int = None
    # 分類
    category: List[str] = []
    # 教授語言
    lecture_language: o_str = None
    # 字幕語言
    subtitle_language: List[str] = []
    # 課程價格
    price: o_str = None
    # ? (html text)
    TA: o_str = None
    # 凸顯部分?
    highlight: Any = None
    # 排程？
    schedule: Any = None
    # 子分類
    subcategory: List[str] = []
    # 是否為自主學習
    is_self_learning: o_bool = None
    # 起始日期
    start_date: o_datetime = None
    # 結束日期
    end_date: o_datetime = None
    # 評估?
    evaluation: Any = None
    # 課前要求
    prerequisites: o_str = None
    # 其他部分
    others: Dict[str, str] = {}
    # 每週時數
    hours_per_week: o_int = None
    # 影片 URL
    video_url: o_str = None
    # 截止日期
    deadline: o_datetime = None
    # 更新日期
    updated_date: o_datetime = None
    # 教學方式
    teaching_method: o_str = None
    # 延伸課程
    extended_course: List[str] = []
    # 內容
    content: o_str = None
    # ?
    pass_standard: o_str = None
    # 證照
    certification: bool = False
    # 證照費用
    certification_fee: o_str = None
    # 媒體類型
    media_type: List[MediaType] = []
    # 學校學期 [-> ?]
    school_semester: o_str = None
    # 媒體數？
    media_count: o_int = None
    # 參考
    references: o_str = None
    # 主體 (html text)
    objective: o_str = None


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
