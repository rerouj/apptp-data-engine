from schemas.LocationSchema import LocationSchema, LocationSchemaLite
from db.gmaps import gmaps
from bson import ObjectId
import wikipediaapi


class LocationController:

    """location controller"""

    name = "location controller"

    def __str__(self):
        return self.name

    @staticmethod
    def add_index(locations_collection):
        """add a numerical index to each value in dataset"""
        for ind, loc in enumerate(locations_collection.find()):
            locations_collection.find_one_and_update({'_id': loc['_id']}, {'$set': {'index': ind + 1}})

    @staticmethod
    def test_wiki_data(archive_name, doc):
        cp_doc = doc
        # res = collection.find_one({'archive_name': archive_name})
        try:
            wiki_data = cp_doc['wiki_data']
            try:
                if len(wiki_data['summary']) > 0:
                    return True
            except KeyError or TypeError:
                return False
        except KeyError or TypeError:
            return False

    @staticmethod
    def add_wiki_data(loc):
        wiki_data = {
            'title': '',
            'summary': ''
        }
        wiki_client = wikipediaapi.Wikipedia('fr')
        if loc == loc.upper():
            loc = loc[0]+loc[1:].lower()
        page = wiki_client.page(loc)
        wiki_data['title'] = page.title
        wiki_data['summary'] = page.summary
        return wiki_data

    @staticmethod
    def dump_show_ids(documents, to_pour, target):
        show_ids_to_pour = []
        for ind in to_pour:
            show_ids_to_pour += documents[ind]['show_id']
        documents[target]['show_id'] += show_ids_to_pour
        return documents

    @staticmethod
    def get_doc_by_regex(expr, collection):

        """merge show ids if country name ambiguity"""

        documents = [doc for doc in collection.find({'archive_name': {"$regex": "{}".format(expr)}})]
        count = len(documents)

        return documents, count

    @staticmethod
    def country_name_disambiguation(documents):

        """merge show ids if country name ambiguity"""

        updated_array = []
        docs = []
        for doc in documents:
            updated_array += doc['show_id']
        for doc in documents:
            cp = doc
            cp['show_id'] = updated_array
            docs.append(cp)
        return docs

    @staticmethod
    def serialize_loc_object(obj):
        schema = LocationSchemaLite()
        res = schema.load(obj)
        return res

    @staticmethod
    def deserialize_loc_object(obj):
        schema = LocationSchemaLite()
        res = schema.dump(obj)
        return res

    @staticmethod
    def save_data(obj, collection_given):
        serialized = LocationController.serialize_loc_object(obj)
        deserialized = LocationController.deserialize_loc_object(serialized)
        res = collection_given.insert_one(deserialized)
        return_object = {'_id': res.inserted_id, 'object': deserialized}
        return return_object

    # deprecated
    @staticmethod
    def serialize_locations_object(collections):
        objects_array = []
        schema = LocationSchema()
        locations = collections['locations']  # mongodb collection
        for location in locations.find():
            if location.get('ggapi_geodata') is None:
                location['_id'] = str(location['_id'])
                res = schema.load(location)
                objects_array.append(res)
        return objects_array

    @staticmethod
    def request_gg_api(location_name=str()):
        if ',' in location_name:
            loc_name_splited = location_name.split(',')
            loc_name_splited.reverse()
            location_name = ', '.join(loc_name_splited)

        res = gmaps.geocode(location_name)
        return res

    @staticmethod
    def arrange_api_data():
        pass

    @staticmethod
    def extract_geo_values(data_subset):

        counter = 0
        locations_extract_arr = []

        for ind, doc in enumerate(data_subset.find()):
            sequences_arr = []
            location_extracted = []
            try:
                seq = [seq for seq in doc['sequences']]
                for location_array in seq:
                    try:
                        sequences_arr.append(location_array['visualGeographicals'])
                    except KeyError:
                        pass
                # unpack sublist values
                location_extracted = [location for sub_list in sequences_arr for location in sub_list]
            except KeyError:
                pass
            try:
                location_extracted += doc['thematicGeographicals']
            except KeyError:
                pass

            location_extracted = list(set(location_extracted))  # get uniq values
            if len(location_extracted) > 0:
                locations_extract_arr.append({'id': doc['id'], 'extract': location_extracted})
            counter += 1

        print(counter)
        return locations_extract_arr

    @staticmethod
    def update_collection(location_extract, show_collection):

        for doc in location_extract:
            # mongodb request
            my_query = {"id": doc['id']}
            new_values = {"$set": {"thematicGeographicalsExtracted": doc['extract']}}
            show_collection.update_one(my_query, new_values)

    @staticmethod
    def create_location_object(show_collection):

        """use LocationSchema and Location class for initiate a location object"""

        """
        for doc in show_collection.find({'thematicGeographicalsExtracted': 'ZÜRICH'},
                                        {'thematicGeographicalsExtracted': 1}):

            locs = doc['thematicGeographicalsExtracted']
            ind = locs.index('ZÜRICH')
            locs[ind] = 'ZURICH'

            show_collection.find_one_and_update({"_id": ObjectId(doc['_id'])},
                                                {"$set": {"thematicGeographicalsExtracted": locs}})
        """

        location_extracted = [doc['thematicGeographicalsExtracted'] for doc in show_collection.find()]
        locations_array = []
        tmp = []
        for arr in location_extracted:
            tmp += arr

        location_extracted = list(set(tmp))
        location_extracted = [obj for obj in location_extracted if obj]
        location_extracted.sort()

        for loc in location_extracted:
            location = {
                "_id": ObjectId(),
                "archive_name": str(),
                "alias": str(),
                "show_id": [()],
                "geo_data": {}
            }
            id_array = []
            for doc in show_collection.find({"thematicGeographicalsExtracted": loc}, {"_id": 1, 'id': 1}):
                id_array.append({'mongo_id': doc['_id'], 'rts_id': doc['id']})
            location['archive_name'] = loc
            location['show_id'] = id_array

            locations_array.append(location)
        return locations_array
