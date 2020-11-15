from pydantic import BaseModel


class Subject(BaseModel):
    name: str
    teacher: str

    class Config:
        orm_mode = True


class SubjectUpdate(Subject):
    name: str = None
    teacher: str = None
