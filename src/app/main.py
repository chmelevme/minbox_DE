from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psycopg2
from .utils import select_pairs, select_product_categories, select_category_products
import os

app = FastAPI()
print(os.getenv('POSTGRES_URL'))


@app.get('/products')
async def get_products():
    conn = psycopg2.connect(
        f'dbname={os.getenv("POSTGRES_DB_NAME")} user={os.getenv("POSTGRES_USER")} password={os.getenv("POSTGRES_PASSWORD")}',
        host=os.getenv('POSTGRES_URL'))
    res = select_product_categories(conn)
    conn.close()
    res_dict = {}
    for item in res:
        res_dict[item[0]] = item[1].split(', ')
    return JSONResponse(res_dict)


@app.get('/categories')
async def get_categories():
    conn = psycopg2.connect(
        f'dbname={os.getenv("POSTGRES_DB_NAME")} user={os.getenv("POSTGRES_USER")} password={os.getenv("POSTGRES_PASSWORD")}',
        host=os.getenv('POSTGRES_URL'))
    res = select_category_products(conn)
    conn.close()
    res_dict = {}
    for item in res:
        res_dict[item[0]] = item[1].split(', ')
    return JSONResponse(res_dict)


@app.get('/pairs')
async def get_pairs():
    conn = psycopg2.connect(
        f'dbname={os.getenv("POSTGRES_DB_NAME")} user={os.getenv("POSTGRES_USER")} password={os.getenv("POSTGRES_PASSWORD")}',
        host=os.getenv('POSTGRES_URL'))
    res = select_pairs(conn)
    conn.close()
    return res
