from pydantic import BaseModel


class createNoteInfo(BaseModel):
    noteTitle: str
    noteContent: str

class deleteNoteInfo(BaseModel):
    noteTitle:str

class updateNoteDateInfo(BaseModel):
    oldTitle:str
    newTitle:str
    noteContent:str


