#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiohttp import web
import asyncio
import json
import pymysql


class RESTController:
    def __init__(self, settings):
        self.settings = settings
        self.db = pymysql.connect(self.settings["db_host"], self.settings["db_user"], self.settings["db_pass"], self.settings["db_name"])
        self.dummy = {
            "products": {
                0: {
                    "name": "Name 1",
                    "description": "Description Product 1",
                    "img": "product01_thumb.png"
                },
                1: {
                    "name": "Name 2",
                    "description": "Description Product 2",
                    "img": "product02_thumb.png"
                },
                2: {
                    "name": "Name 3",
                    "description": "Description Product 3",
                    "img": "product03_thumb.png"
                },
                3: {
                    "name": "Name 4",
                    "description": "Description Product 4",
                    "img": "product04_thumb.png"
                }
            },
            "locations_details": {
                0: {
                    "name": "Aldi Frankfurt",
                    "description": "Huh, idk?",
                    "address": "Frankfurt am Main"
                },
                1: {
                    "name": "Aldi München",
                    "description": "Huh, idk?",
                    "address": "München"
                },
                2: {
                    "name": "Aldi Hamburg",
                    "description": "Huh, idk?",
                    "address": "Frankfurt am Hamburg"
                }
            },
            "pax_data": {
                0: {
                    "count": 12,
                    "presence_time": 580
                },
                1: {
                    "count": 17,
                    "presence_time": 870
                },
                2: {
                    "count": 44,
                    "presence_time": 1230
                }
            },
            "locations_stats": {
                0: 1,
                1: 1,
                2: 0
            },
            "results": [0, 1, 2],
            "locations_stock": {
                0: {
                    0: 2,
                    1: 1,
                    3: 0,
                    4: 1
                },
                1: {
                    0: 1,
                    1: 0,
                    3: 2,
                    4: 2
                }
            },
            "results_": [
                {
                    "market_id": 0,
                    "distance": 500,
                    "civilStatus": 0,
                    "products": {
                        "2": {
                            "status": 0,
                            "lastUpdate": 1584790887
                        },
                        "3": {
                            "status": 2,
                            "lastUpdate": 1584790887
                        },
                        "6": {
                            "status": 1,
                            "lastUpdate": 1584790887
                        }
                    }
                }
            ],
            "pax_count": {}
        }

    async def search(self, request):
        result = []
        try:
            query = await request.json()
            location = {
                "lat": float(query["lat"]),
                "lon": float(query["lon"]),
                "products": list(filter(lambda elm: isinstance(elm, int), query["products"])),
                "radius": 5000
            }
        except:
            location = None

        if location is not None:
            if "radius" in query:
                radius = int(query["radius"])
                if radius > 0:
                    location["radius"] = radius

            # Do some queries against the DB
            # '''SELECT * FROM locations WHERE '''
            # DUMMY: unfiltered!
            cursor = self.db.cursor()
            cursor.execute('''SELECT id FROM market''')
            location_ids = cursor.fetchall()
            for location_id in location_ids:
                result.append(location_id[0])
            cursor.close()

        return web.json_response(result)

    async def getLocationsDetails(self, request):
        try:
            location_ids = await request.json()
        except:
            location_ids = []

        result = []

        if isinstance(location_ids, list) and len(location_ids) > 0:
            location_ids = list(filter(lambda elm: isinstance(elm, int), location_ids))
            cursor = self.db.cursor()
            query = '''SELECT id, name, address, ltdtude, lngtude FROM market WHERE id in (%s)''' % ",".join(
                ["%s"] * len(location_ids))
            cursor.execute(query, tuple(location_ids))
            market_details = cursor.fetchall()
            for market_detail in market_details:
                #array and append
                result.append({
                    "id": market_detail[0],
                    "name": market_detail[1],
                    "address": market_detail[2],
                    "ltdtude": market_detail[3],
                    "lngtude": market_detail[4]
                })
            cursor.close()

        return web.json_response(result)

    async def _getLocationsPax(self, location_ids):
        result = []

        if isinstance(location_ids, list) and len(location_ids) > 0:
            location_ids = list(filter(lambda elm: isinstance(elm, int), location_ids))
            cursor = self.db.cursor()
            query = '''SELECT market_id, pax_count, average_presence_time FROM market_pax WHERE market_id IN (%s) ORDER BY timestamp DESC LIMIT 1''' % ",".join(["%s"]*len(location_ids))

            cursor.execute(query,tuple(location_ids))
            pax_lines = cursor.fetchall()
            for pax_line in pax_lines:
                result.append({
                    "location_id": pax_line[0],
                    "pax_count": pax_line[1],
                    "average_presence_time": pax_line[2]
                })

            cursor.close()
        return result

    async def getLocationsPax(self, request):
        try:
            location_ids = await request.json()
        except:
            location_ids = []
        return web.json_response(await self._getLocationsPax(location_ids))

    async def _getLocationsStats(self, location_ids):
        result = []
        if isinstance(location_ids, list) and len(location_ids) > 0:
            location_ids = list(filter(lambda elm: isinstance(elm, int), location_ids))
            cursor = self.db.cursor()

            query = 'SELECT sts.id, sts.ranking FROM sichereseinkaufen.market_stats as sts WHERE sts.market_id in (%s) order by timestamp DESC LIMIT 1'  % ",".join(["%s"]*len(location_ids))

            cursor.execute(query, tuple(location_ids))
            locationsstats = cursor.fetchall()
            stats_lines = cursor.fetchall()
            for stats_line in stats_lines:
                result.append = ({
                    "location_id": stats_line[0],
                    "ranking": stats_line[1]
                })

            cursor.close()
        return locationsstats

    async def getLocationsStats(self, request):
        try:
            location_ids = await request.json()
        except:
            location_ids = []

        return web.json_response(await self._getLocationsStats(location_ids))


    async def _getLocationsStock(self, location_ids, product_ids):
        #DUMMY: DB data needed here
        return self.dummy["locations_stock"]

    async def getLocationsStock(self, request):
        try:
            data = await request.json()
            data = {
                "product_ids": data["product_ids"],
                "location_ids": data["location_ids"]
            }
        except:
            data = None

        result = {}
        if data is not None:
            if isinstance(data["product_ids"], list) and isinstance(data["location_ids"], list):
                data["product_ids"] = list(filter(lambda elm: isinstance(elm, int), data["product_ids"]))
                data["location_ids"] = list(filter(lambda elm: isinstance(elm, int), data["location_ids"]))
                result = await self._getLocationsStock(data["location_ids"], data["product_ids"])
        return web.json_response(result)

    async def getProducts(self, request):
        cursor = self.db.cursor()
        cursor.execute('''SELECT id, product_name FROM products''')
        products = cursor.fetchall()
        response = {}
        for product in products:
            response[product[0]] = product[1]
        return web.json_response(response)

    async def addLocationRating(self, request):
        return web.Response()

    async def addLocationStock(self, request):
        return web.Response()
