import asyncio
import aiomysql
import aiohttp


BOOKS_API_URL = 'https://fakerapi.it/api/v1/books?_quantity={quantity}'

loop = asyncio.get_event_loop()
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'SleepHat',
    'db': 'test',
    'autocommit': True,
}


# async def get_all_book_from_db(loop):
#     conn = await aiomysql.connect(host='127.0.0.1', port=3306,
#                                        user='root', password='SleepHat',
#                                        db='test', loop=loop)
#     async with conn.cursor() as cur:
#         await cur.execute('SELECT * FROM music_style')
#         r = await cur.fetchall()
#
#         await cur.close()
#
#     conn.close()
#     return r


async def add_book_to_db(
        title: str,
        autor: str,
        publish_year: int,
        isbn: str
):
    conn = await aiomysql.connect(**DB_CONFIG)
    async with conn.cursor() as cur:
        sql_query = "INSERT INTO books (title, autor, publish_year, isbn) VALUES (%s, %s, %s, %s)"
        await cur.execute(sql_query, (title, autor, publish_year, isbn))

        await cur.close()

    conn.close()
    return True


async def get_book_isbn_from_db(
        isbn: str,
):
    conn = await aiomysql.connect(**DB_CONFIG)
    async with conn.cursor() as cur:
        sql_query = f"SELECT * FROM books WHERE isbn = {isbn}"
        await cur.execute(sql_query)
        book = await cur.fetchone()

    conn.close()
    return book


async def delete_book_from_db(
        book_id: int,
):
    conn = await aiomysql.connect(**DB_CONFIG)
    async with conn.cursor() as cur:
        sql_query = f"DELETE FROM books WHERE id = {book_id}"
        await cur.execute(sql_query)

    conn.close()
    return [True, "deleted"]


async def fetch_books_from_api(quantity: int=5000):
    async with aiohttp.ClientSession() as session:
        async with session.get(BOOKS_API_URL.format(quantity=quantity)) as response:
            if response.status != 200:
                return [False, {}]
            data_books = await response.json()
            data_books = data_books.get("data")
            for book in data_books:
                await add_book_to_db(
                    title=book.get("title"),
                    autor=book.get("author"),
                    publish_year=int(book.get("published")[:4]),
                    isbn=book.get("isbn"),
                )
            return [True, await response.json()]
