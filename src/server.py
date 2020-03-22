#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiohttp import web
from RESTController import RESTController



def main():
    rc = RESTController("foo")
    app = web.Application()
    app.add_routes([
        web.post('/api/search', rc.search),
        web.get('/api/locations/details',  rc.getLocationsDetails),
        web.get('/api/locations/pax', rc.getLocationsPax),
        web.get('/api/locations/stats', rc.getLocationsStats),
        web.get('/api/locations/stock', rc.getLocationsStock),
        web.get('/api/products', rc.getProducts)
        ])
    web.run_app(app, port=8085)

if __name__ == "__main__":
    main()