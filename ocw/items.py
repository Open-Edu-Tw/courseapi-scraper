# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime
from enum import Enum
from typing import Optional, Any, List, Dict

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
    """
    媒體類型。

    VIDEO - 影片
    SLIDE - 簡報
    PAPER - PDF/DOCX/ODF 等紙本文件
    UNKNOWN - 未定義類型
    """
    VIDEO = "video"
    SLIDE = "slide"
    PAPER = "paper"
    UNKNOWN = "unknown"


class TypedCourseItem(BaseModel):
    """
    一個課程的各個資訊。

    關於每個欄位的說明，可見 TypedCourseItem 的程式碼。
    """
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
