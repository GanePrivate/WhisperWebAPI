from pydantic import BaseModel, Field


class UploadResponseModel(BaseModel):
    text: str = Field(...)


class UploadErrorResponseModel(BaseModel):
    detail: str = '文字起こし処理に失敗しました'