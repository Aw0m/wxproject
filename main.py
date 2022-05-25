# coding:utf-8
# author:liushuwen
# creation:2022-5-23

from typing import *
from fastapi import *
from model import *
import uvicorn
import pymysql

# 连接数据库
try:
    db = pymysql.connect(host="localhost",
                         user="root",
                         password="@Mysql5",
                         database="MySQL_lan",
                         port=3306)
except:
    print("数据库连接失败")
    exit(-1)

# 初始化
cursor = db.cursor()
app = FastAPI()


# 创建笔记

@app.post("/api/note/createNote")
async def createNote(info: createNoteInfo,userID: Union[str, None] = Header(default=None)):
    noteTitle = info.noteTitle
    noteContent = info.noteContent
    print(userID, noteTitle, noteContent)
    if userID and noteTitle:
        noteTitle = str(noteTitle)
        noteContent = str(noteContent)
        sql = "INSERT INTO note (userID,title,content) VALUES ('%s','%s','%s')" % (
            userID, noteTitle, noteContent)
        try:
            # 执行语句
            cursor.execute(sql)
            # 提交到数据库
            db.commit()
        except:
            # 发生错误就回滚
            db.rollback()
            return {"error": "数据库提交失败"}
        db.close()
        return {"msg": "ok"}
    return {"error": "无数据传入"}


# 删除笔记
@app.post("/api/note/deleteNote")
async def deleteNote(info: deleteNoteInfo, userID: Union[str, None] = Header(default=None)):
    noteTitle = info.noteTitle
    if userID and noteTitle:
        sql = "DELETE FROM note WHERE userID='%s' AND title='%s'" % (
            userID, noteTitle)
        try:
            # 执行语句
            cursor.execute(sql)
            # 提交到数据库
            db.commit()

        except:
            # 发生错误就回滚
            db.rollback()
            return {"error": "数据库提交失败"}
        db.close()
        return {"msg": "ok"}
    return {"error": "无数据传入"}


# 更新笔记
@app.post("/api/note/updateNoteDate")
async def updateNoteDate(info:updateNoteDateInfo,userID: Union[str, None] = Header(default=None)):
    oldTitle=info.oldTitle
    newTitle=info.newTitle
    noteContent=info.noteContent
    if userID and oldTitle and newTitle:
        sql = "UPDATE note SET title='%s',content='%s' WHERE id='%s' AND title='%s'" % (
            newTitle, noteContent, userID, oldTitle)
        try:
            # 执行语句
            cursor.execute(sql)
            # 提交到数据库
            db.commit()
            # 获取数据

        except:
            # 发生错误就回滚
            db.rollback()
            return {"error": "数据库提交失败"}
        db.close()
        return {"msg": "ok"}
    return {"error": "无数据传入"}


# 获取笔记列表
@app.get("/api/note/getNoteList")
async def getNoteList(userID: Union[str, None] = Header(default=None)):
    if userID:
        sql = "SELECT title FROM note WHERE userID='%s'" % (userID)
        try:
            # 执行语句
            cursor.execute(sql)
            # 提交到数据库
            db.commit()
            # 获取数据
            data = cursor.fetchall()

        except:
            # 发生错误就回滚
            db.rollback()
            return {"error": "数据库提交失败"}
        db.close()
        return data
    return {"error": "无数据传入"}


# 获取笔记数据
@app.get("/api/note/getNote")
async def getData(noteTitle: getDataInfo,userID: Union[str, None] = Header(default=None)):
    if userID and noteTitle:
        sql = "SELECT content FROM note WHERE userID='%s' AND title='%s'" % (
            userID, noteTitle)
        try:
            # 执行语句
            cursor.execute(sql)
            # 提交到数据库
            db.commit()
            # 获取数据
            data = cursor.fetchall()

        except:
            # 发生错误就回滚
            db.rollback()
            return {"error": "数据库提交失败"}
        db.close()
        return data
    return {"error": "无数据传入"}


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1",
                port=8000, reload=True, debug=True)
