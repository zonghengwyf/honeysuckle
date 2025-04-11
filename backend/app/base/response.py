from fastapi.responses import JSONResponse
from typing import Any, Dict

class BaseResponse(JSONResponse):
    def __init__(self, data: Any=None, message: str="", status_code: int = 200) -> None:
        content = {"message": message}
        if not data is None: content.update({"data": data})
        super().__init__(content=content, status_code=status_code)

    @classmethod
    def not_found(cls, message: str = "Resource not found") -> "BaseResponse":
        return cls(data=None, message=message, status_code=404)

    @classmethod
    def error(cls, message: str) -> "BaseResponse":
        return cls(data=None, message=message, status_code=400)