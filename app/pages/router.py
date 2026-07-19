from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

from app.hotels.router import get_hotels

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

env = Environment(loader=FileSystemLoader("app/templates"))

@router.get("/hotels", response_class=HTMLResponse)
async def get_hotels_page(
    request: Request,
    hotels=Depends(get_hotels)
    ):
    template = env.get_template("hotels.html")
    html_content = template.render(
        request=request,
        hotels=hotels,
        url_for = request.url_for
        )
    return HTMLResponse(content=html_content)
