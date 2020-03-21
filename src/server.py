#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiohttp import web
from RESTController import RESTController

def main():
    rc = RESTController("foo")
    app = web.Application()
    app.add_routes([
        #web.post('/API/search', rc.search),
        web.get('/API/locations', rc.getLocations),
        web.get('/API/products', rc.getProducts)
        ])
    web.run_app(app)

if __name__ == "__main__":
    main()