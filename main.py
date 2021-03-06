# coding:utf-8
# author:liushuwen
# creation:2022-5-23
import json
from typing import *
from fastapi import *
from model import *
import uvicorn
import pymysql
from service_registry import RegistryThread

# 连接数据库
try:
    with open('database.json', 'r', encoding='utf8') as fp:
        config = json.load(fp)
        fp.close()
    db = pymysql.connect(host=config["host"],
                         user=config["user"],
                         password=config["password"],
                         database=config["database"],
                         port=config["port"])
except:
    print("MySQL数据库连接失败")
    exit(-1)

# 初始化
cursor = db.cursor()
app = FastAPI()


# 创建笔记

@app.post("/api/note/createNote")
async def createNote(info: createNoteInfo, userID: Union[str, None] = Header(default=None)):
    noteTitle = info.noteTitle
    noteContent = info.noteContent
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
        # obtainOder="SELECT id FROM note WHERE userID='%s'AND title='%s'" % (
        #     userID, noteTitle)

        try:
            cursor.execute(sql)
            # keep id's order
            # cursor.execute(obtainOder)
            # db.commit()
            # order = cursor.fetchall()
            # order=int(order)
            # keepOrder = "alter table note AUTO_INCREMENT='%d'"%(order+1)
            # cursor.execute(keepOrder)
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
async def updateNoteDate(info: updateNoteDateInfo, userID: Union[str, None] = Header(default=None)):
    oldTitle = info.oldTitle
    newTitle = info.newTitle
    noteContent = info.noteContent
    if userID and oldTitle and newTitle:
        sql = "UPDATE note SET title='%s',content='%s' WHERE userID='%s' AND title='%s'" % (
            newTitle, noteContent, userID, oldTitle)
        try:
            # 执行语句
            cursor.execute(sql)
            # 提交到数据库
            db.commit()
            # 获取数据

        except Exception as e:
            print(e)
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
async def getData(noteTitle, userID: Union[str, None] = Header(default=None)):
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


        except Exception as e:
            print(e)
            # 发生错误就回滚
            db.rollback()
            return {"error": "数据库提交失败"}
        db.close()
        return data
    return {"error": "无数据传入"}


if __name__ == '__main__':
    r = RegistryThread("note", "116.63.145.25", "8002", 3)
    r.start()
    uvicorn.run(app='main:app', host="0.0.0.0", port=8002, reload=True, debug=True)
