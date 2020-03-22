#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiohttp import web
import asyncio
import json


class RESTController:
    def __init__(self, db):
        self.db = db
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
            query = request.query
            location = {
                "lat": float(query["lat"]),
                "lon": float(query["lon"]),
                "radius": 5000
            }
        except:
            location = None
        
        if "radius" in query:
            radius = int(query["radius"])
            if radius > 0:
                location["radius"] = radius
        
        if location is not None:
            # Do some queries against the DB
            #'''SELECT * FROM locations WHERE '''

            # But for now something static
            result = self.dummy["results"]
        print(location)
        return web.json_response(result)

    async def getLocationsDetails(self, request):
        try:
            query = request.query
            location_ids = json.loads(query["location_ids"])
        except:
            location_ids = []
        
        result = {}

        if isinstance(location_ids, list):
            location_ids = list(filter(lambda elm: isinstance(elm, int), location_ids))
            for location_id in location_ids:
                if location_id in self.dummy["locations_details"]:
                    result[location_id] = self.dummy["locations_details"][location_id]

        return web.json_response(result)



    async def _getLocationsPax(self, location_ids):
        # DUMMY: get it from DB, calculate it over time
        return self.dummy["pax_data"]

    async def getLocationsPax(self, request):
        try:
            query = request.query
            location_ids = json.loads(query["location_ids"])
        except:
            location_ids = []
        return web.json_response(await self._getLocationsPax(location_ids))
    




    async def _getLocationsStats(self, location_ids):
        # DUMMY: get it from DB, calculate it over time
        return self.dummy["locations_stats"]

    async def getLocationsStats(self, request):
        try:
            query = request.query
            location_ids = json.loads(query["location_ids"])
        except:
            location_ids = []
        return web.json_response(await self._getLocationsStats(location_ids))



    async def _getLocationsStock(self, location_ids, product_ids):
        #DUMMY: DB data needed here 
        return self.dummy["locations_stock"]

    async def getLocationsStock(self, request):
        return web.json_response(self._getLocationsStock([],[]))
        


    async def getProducts(self, request):
        return web.json_response(self.dummy["products"])
    
