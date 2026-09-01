from pydantic import BaseModel, ConfigDict, Field


class CategoryDistributionItem(BaseModel):
    category: str
    count: int = Field(ge=0)


class AdminDashboardStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_distribution: list[CategoryDistributionItem]
