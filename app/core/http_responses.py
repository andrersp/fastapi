# -*- coding: utf-8 -*-
from typing import List
from fastapi.responses import JSONResponse

from app.ext.exceptions import CustomException


response_schema = {

    201: {
        "description": "Send Report",
        "content": {
            "application/json": {
                "example": {"success": True}
            }
        },
    },

    200: {
        "description": "Get Person",
        "content": {
            "application/json": {
                "example": {"success": True, "data": [{"name": "Person Name"}]}
            }
        },
    },
}


def success(params: dict = {}, status_code: int = 200):

    response = params.copy()

    response.update({"success": True})

    return JSONResponse(status_code=status_code, content=response)


def error(params: List[str] = [], status_code: int = 400):

    response = {"success": False}
    response.update({'errors': params})

    return JSONResponse(status_code=status_code, content=response)
