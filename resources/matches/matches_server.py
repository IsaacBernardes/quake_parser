from fastapi import APIRouter, Response
from resources.matches.resources_matches_listall import listall_handler

router = APIRouter()


@router.get("/matches")
def list_all_matches(response: Response):
    status_code, data = listall_handler()
    response.status_code = status_code
    return data


@router.get("/matches/{match_id}")
def find_one_match(match_id: str, response: Response):
    status_code, data = listall_handler({"match_id": match_id})
    response.status_code = status_code
    return data
