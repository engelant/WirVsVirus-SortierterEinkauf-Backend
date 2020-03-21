from aiohttp import web

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
            "locations": {
                0: {
                    "name": "Aldi Frankfurt"
                },
                1: {
                    "name": "Rewe Mannheim"
                },
                2: {
                    "name": "Kaufland Heidelberg"
                }
            }
        }
    
    async def search(self, request):
        rd = await request.json()
        #rd now should have user Input, propably a good idea to check everything, especially types

        #Do some queries against the DB
        #'''SELECT * FROM locations WHERE ''' 

        #But for now something static
        result = [
            {
                "marketID": 0,
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
        ]
        return web.json_response(result)

    async def getLocations(self, request):
        result = {}
        try:
            rd = await request.json()
        except:
            rd = None

        #rd is user input and should be a list of IDs
        if isinstance(rd, list):
            rd = list(dict.fromkeys(rd))
            for locationID in rd:
                if isinstance(locationID, int):
                    
                    #DUMMY: grab the location info by the the locationID
                    if locationID in self.dummy["locations"]:
                        result[locationID] = self.dummy["locations"][locationID]

        #returns an object of LocationID
        

        return web.json_response(result)


    async def getProducts(self, request):
        return web.json_response(self.dummy["products"])