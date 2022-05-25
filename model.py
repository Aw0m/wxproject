from pydantic import BaseModel


class Info(BaseModel):
    noteTitle: str
    noteContent: str
