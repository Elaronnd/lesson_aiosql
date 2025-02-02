from aiohttp import web
from test_db import add_book_to_db, get_book_isbn_from_db

async def get_book_by_isbn(request):
    isbn = request.query.get('isbn')
    book = await get_book_isbn_from_db(isbn=isbn)
    return web.json_response({'book': book})


async def add_book(request):
    data = await request.json()
    title = data.get('title')
    author = data.get('author')
    publish_year = data.get('publish_year')
    isbn = data.get('isbn')

    if not all([title, author, publish_year, isbn]):
        return web.json_response({'msg': 'Не вистачає інформації.'}, status=400)

    await add_book_to_db(
        title=title,
        autor=author,
        publish_year=publish_year,
        isbn=isbn,
    )
    return web.json_response({'msg': 'Книгу додано.'})


def main():
    app = web.Application()
    app.router.add_get(path="/book/isbn", handler=get_book_by_isbn)
    app.router.add_post(path='/book/add', handler=add_book)

    return app

if __name__ == '__main__':
    app = main()
    web.run_app(app=app, host='0.0.0.0', port=80)
