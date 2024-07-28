from beanie import Document
from pydantic.fields import Field


class SiteViewer(Document):
    record_time: str = Field(..., description="日期", examples=["1970-01-01"])
    hour: int = Field(..., description="时间", examples=[1])
    view: int = Field(..., description="访问链接", examples=[0])

    class Settings:
        name = "siteviews"
