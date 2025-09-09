from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.demo_controller import DemoController
from app.schemas.demo_schema import DemoCreate, DemoResponse

router = APIRouter()


@router.post("/", response_model=DemoResponse)
def create_demo(demo: DemoCreate, db: Session = Depends(get_db)):
    controller = DemoController(db)
    return controller.create_demo(demo)


@router.get("/", response_model=list[DemoResponse])
def get_demos(db: Session = Depends(get_db)):
    controller = DemoController(db)
    return controller.get_all_demos()


@router.get("/id/{demo_id}", response_model=DemoResponse)
def get_demo_by_id(demo_id: int, db: Session = Depends(get_db)):
    controller = DemoController(db)
    return controller.get_demo_by_id(demo_id)


@router.get("/email/{demo_email}", response_model=DemoResponse)
def get_demo_by_email(demo_email: str, db: Session = Depends(get_db)):
    controller = DemoController(db)
    return controller.get_demo_by_email(demo_email)
