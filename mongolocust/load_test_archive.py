from locust import between
from settings import DEFAULTS
DEFAULTS['CLUSTER_URL'] = DEFAULTS['ARCHIVE_URL']

from mongo_user import MongoUser, mongodb_task


import pymongo
import random
from datetime import datetime, timedelta
import pprint

pp = pprint.PrettyPrinter(indent=4)

MIN_DATE = datetime.fromisoformat('2021-10-10T00:00:00')
MAX_DATE = datetime.fromisoformat('2022-04-08T00:00:00')
MAX_EQUIPMENT = 37155

class MongoSampleUser(MongoUser):
    """
    Generic sample mongodb workload generator
    """
    # no delays between operations
    wait_time = between(0.0, 0.0)

    def __init__(self, environment):
        super().__init__(environment)

    @mongodb_task(1)
    def run_query(self):
        first_equipment = random.randint(0, MAX_EQUIPMENT)
        second_equipment = random.randint(0, MAX_EQUIPMENT)
        
        random_num_days_after_min_date = random.randrange((MAX_DATE-MIN_DATE).days)
        query_start_date = MIN_DATE + timedelta(days=random_num_days_after_min_date)
        query_end_date = query_start_date + timedelta(days=7)

        projection = {"_id":0, "meta.id": 1, "ts": 1}
        while len(projection) < 6:
            rand_measure = 'measure' + str(random.randint(1, 19))
            projection["measurements." + rand_measure] = 1


        query = [
            {
                '$match': {
                    "$and":
                    [
                        {"$or":
                            [{'meta.id': first_equipment}, {'meta.id': second_equipment}]
                         },
                        {"ts":
                            {"$gte": query_start_date, "$lt": query_end_date}
                         }
                    ],
                }
            },
            {
                '$project': projection
            },
            {
                '$match': {
                    'measurements': {
                        '$ne': {}
                    }
                }
            }
        ]
        pp.pprint(query);
        results = list(self.collection.aggregate(query))
        print(len(results))
        #pp.pprint(results);
        return results

    def on_start(self):
        """
        Executed every time a new test is started - place init code here
        """
        # prepare the collection
        self.collection, self.collection_secondary = self.ensure_collection(DEFAULTS['COLLECTION_NAME'], [])


