import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict,Union
from datetime import datetime,date,timedelta
import pandas as pd
import numpy as np
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
cur=None
conn=None
app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    global conn
    conn = psycopg2.connect(
        database="book", # database name
        user = "postgres", # user name
        password = "c#@ndru 12", #password
        host = "localhost", # host
        port = "5432" # port number enabled by you
    )
    global cur
    cur = conn.cursor()
@app.on_event("shutdown")
async def shutdown():
    await conn.commit()
    await conn.close()

table_name1="user"
class user(BaseModel):
    userID:int = Field(..., example=1001)
    userName: str = Field(..., example="Manjot Singh")
    password: str = Field(..., example=200)
    email : str = Field(..., example=2)
class Update_user(BaseModel):
    userID: int = Field(..., example="Enter Empname")
    userName: str = Field(..., example="Enter TagId")
    email: str = Field(..., example="Enter Role")

def get_data_as_json(lt):
    ans = []
    print(lt)
    for row in lt:
        temp = { 'userID' : row[0], 'userName': row[1], 'email': row[3] }
        ans.append(temp)
    return ans

table_name1="user"

@app.get('/getAllUsers')
async def all_users():
    cur.execute(f'SELECT * FROM "{table_name1}"')
    return get_data_as_json(cur.fetchall())

class login(BaseModel):
    email:str = Field(..., example=102)
    password:str = Field(..., example='emp102')

def get_data_as_json2(lt):
    temp={}
    for row in lt:
        temp = { 'userID' : row[0], 'userName': row[1] , 'status':'login successfull!'}
    return temp

@app.post('/login')
async def validate_login(login_val:login):
    cur.execute(f'SELECT "userID","userName" from  "{table_name1}" where "email"=\'{login_val.email}\' and "password"=\'{login_val.password}\'')
    res=cur.fetchall()
    data=list(res)
    if len(data)==0:
        return {"message":"Invalid Username/Password"}   
    return get_data_as_json2(res)

# class reading(BaseModel):
#     email:str = Field(..., example=102)
#     password:str = Field(..., example='emp102')


def get_data_as_json3(lt):
    ans=[]
    temp={}
    for row in lt:
        temp = { 'bookID' : row[0], 'title': row[1] , 'author/genre': row[2] }
        ans.append(temp)    
    return ans

@app.get('/listByGenre')
async def browseaddby_genre(ipgenre:str):
    cur.execute(f'SELECT "bookID",title,author from public.books where genre=\'{ipgenre}\'')
    res=cur.fetchall()
    print(res)
    return get_data_as_json3(res) 

@app.get('/listByAuthor')
async def browseaddby_genre(ipauthor:str):
    cur.execute(f'SELECT "bookID",title,genre from public.books where genre=\'{ipauthor}\'')
    res=cur.fetchall()
    print(res)
    return get_data_as_json3(res) 


@app.post('/addRreadingList')
async def addReadingList(userID:int,bookID:int):
    cur.execute(f'INSERT INTO public."readingList" ("bookID", "userID") VALUES ({bookID}, {userID})')
    conn.commit()

    return {"status":"added to reading list successfully"}

def get_data_as_json4(lt):
    ans=[]
    temp={}
    for row in lt:
        temp = { 'bookID' : row[0], 'title': row[1] , 'author': row[2], 'genre':row[3] , 'num_pages':row[4] }
        ans.append(temp)    
    return ans


@app.get('/listAllBooks')
async def listAllBooks():
    cur.execute(f'SELECT * from public.books')
    res=cur.fetchall()
    print(res)
    return get_data_as_json4(res) 

@app.post('/addColectionList')
async def addCollectionList(userID:int,bookID:int):
    cur.execute(f'INSERT INTO public.collection ("userID", "bookID") VALUES ({userID}, {bookID});')
    conn.commit()
    return {"status":"added to collection list successfully"}

@app.get('/listCollection')
async def listAllBooks():
    cur.execute(f'SELECT * from public.collections')
    res=cur.fetchall()
    print(res)
    return get_data_as_json4(res)


def get_data_as_json6(lt):
    temp={}
    for row in lt:
        temp = { 'bookID' : row[0], 'title': row[1] , 'author': row[2], 'genre': row[3], 'num_pages': row[4]}
    return temp

@app.get('/searchBookbyName')
async def listBook(bname:str):
    cur.execute(f'SELECT "bookID", title, author, genre, num_pages FROM public.books where title=\'{bname}\'')
    res=cur.fetchall()
    print(res)
    return get_data_as_json6(res)


@app.get('/searchBookbyAuthor')
async def listBook(author:str):
    cur.execute(f'SELECT "bookID", title, author, genre, num_pages FROM public.books where author=\'{author}\'')
    res=cur.fetchall()
    print(res)
    return get_data_as_json6(res)    

@app.post('/addFavorites')
async def addFavoriteList(userID:int,bookID:int):
    cur.execute(f'INSERT INTO public.favorites ("userID", "bookID") VALUES ({userID},{bookID} );')
    conn.commit()
    return {"status":"added to Favorite list successfully"}