from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import string
import random
from faker import Faker

conn = MongoClient('<CONNECTION_STRING>')
print("Connected successfully!!!")

# database
db = conn.pic
collection = db.equipos

NUM_DEVICES = 37155
# 25% del nymero real de equipos

START_WITH_DEVICE = 0
NUM_EVENTS = 146327
# Numero de eventos por dispositivo en 6 meses
#  65242 Millones de datos / 148621 dispositivos / 3 datos por evento

MILLISECS_DELTA_BETWEEN_EVENTS = 106282
# Calculado para que los timestamps se extiendan por unos 6 meses

NUM_MEASUREMENTS_CHANGED_PER_EVENT = 3

BATCH_SIZE = 50000
# No relacionado con el modelo ni la volumetria, simplemente agrupamos operaciones y las ejecutamos en un batch

faker = Faker()

FIRST_TS = datetime.now()

def generate_base_document(device_id):
# Genera un documento inicial con los metadatos del equipo
# y un valor inicial para todas sus medidas
        document = {
                'ts': FIRST_TS,
                "meta": {
                        "id": device_id,
                        "extra_atrib1": faker.pystr(6,6),
                        "extra_atrib2": faker.pystr(6,6),
                        "extra_atrib3": faker.pystr(6,6),
                        "extra_atrib4": faker.pystr(6,6),
                        "extra_atrib5": faker.pystr(6,6),
                        "extra_atrib6": faker.pystr(6,6),
                        "extra_atrib7": faker.pystr(6,6),
                        "extra_atrib8": faker.pystr(6,6),
                        "extra_atrib9": faker.pystr(6,6),
                        "extra_atrib10": faker.pystr(6,6),
                        "extra_atrib11": faker.pystr(6,6),
                        "extra_atrib12": faker.pystr(6,6),
                        "extra_atrib13": faker.pystr(6,6),
                        "extra_atrib14": faker.pystr(6,6),
                        "extra_atrib15": faker.pystr(6,6),
                        "extra_atrib16": faker.pystr(6,6),
                        "extra_atrib17": faker.pystr(6,6),
                        "extra_atrib18": faker.pystr(6,6),
                        "extra_atrib19": faker.pystr(6,6)
                },
                'measurements': {
                        "measure1": round(random.uniform(0, 50), 2),
                        "measure2": round(random.uniform(0, 50), 2),
                        "measure3": round(random.uniform(0, 50), 2),
                        "measure4": round(random.uniform(0, 50), 2),
                        "measure5": round(random.uniform(0, 50), 2),
                        "measure6": round(random.uniform(0, 50), 2),
                        "measure7": round(random.uniform(0, 50), 2),
                        "measure8": round(random.uniform(0, 50), 2),
                        "measure9": round(random.uniform(0, 50), 2),
                        "measure10": round(random.uniform(0, 50), 2),
                        "measure11": round(random.uniform(0, 50), 2),
                        "measure12": round(random.uniform(0, 50), 2),
                        "measure13": round(random.uniform(0, 50), 2),
                        "measure14": round(random.uniform(0, 50), 2),
                        "measure15": round(random.uniform(0, 50), 2),
                        "measure16": round(random.uniform(0, 50), 2),
                        "measure17": round(random.uniform(0, 50), 2),
                        "measure18": round(random.uniform(0, 50), 2),
                        "measure19": round(random.uniform(0, 50), 2)
                }
        }
        return document

def next_doc_to_insert(doc):
# Se le pasa como parametro el documento base
# actualiza 3 valores de medidas en el doc base
# y genera un documento para insertar con los mismos metadatos y que solo contiene
# las medidas que han cambiado
        doc['ts'] += timedelta(milliseconds = MILLISECS_DELTA_BETWEEN_EVENTS)        
        newDoc = doc.copy()
        newDoc['measurements'] = {}
        
        for _ in range(NUM_MEASUREMENTS_CHANGED_PER_EVENT):
                already_updated = set()
                measure_to_update = 'measure' + str(random.randint(1, 19))
                while measure_to_update in already_updated:
                        measure_to_update = 'measure' + str(random.randint(1, 19))
                old_value = doc['measurements'][measure_to_update]
                doc['measurements'][measure_to_update] = old_value + round(random.uniform(-2, 2), 2)
                newDoc['measurements'][measure_to_update] = doc['measurements'][measure_to_update]
                already_updated.add(measure_to_update)
        newDoc['measurements'] = dict(sorted(newDoc['measurements'].items()))
        return newDoc


# Bucle principal que genera e inserta documentos
docs = []
for d in range(START_WITH_DEVICE, NUM_DEVICES):
        doc = generate_base_document(d)
        for e in range(NUM_EVENTS):
                doc_to_insert = next_doc_to_insert(doc);
                docs.append(doc_to_insert);
                if len(docs) == BATCH_SIZE:
                        collection.insert_many(docs)
                        docs = []
                        print("Batch inserted")
        if len(docs) > 0:
                collection.insert_many(docs)
                docs = []
        print("Inserted all events for device: " + str(d))


