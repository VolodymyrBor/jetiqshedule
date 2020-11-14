from pydantic import BaseModel


class Subject(BaseModel):
    name: str
    teacher: str
