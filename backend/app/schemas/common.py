from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict

DataT = TypeVar("DataT")


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    message: str


class ApiResponse(BaseResponse, Generic[DataT]):
    data: DataT | None = None


class ErrorResponse(BaseResponse):
    success: Literal[False] = False
    data: None = None
