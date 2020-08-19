from globals import *
from controllers.LocationController import LocationController as lc
from bson import ObjectId
from db import db
from functools import reduce
from pymongo import ReturnDocument


class LocationViews:

    """Locations views"""

    def __init__(self, collections):
        self.db = db.db
        self.collections = collections
        self.views_freq = 2
        self.locations_array = []
        self.location_objects = []

    def home_view(self):
        while True:
            print(LOCATION_VIEW_WELCOME_STR)
            ans = input('value:')
            if ans == 'e':
                break
            elif ans == '1':
                self.extract_geo_values_view()
            elif ans == '2':
                self.add_missing_values_view()
            elif ans == '3':
                self.prepare_location_object_view()
            elif ans == '4':
                self.add_geo_data_view()
            elif ans == '5':
                self.disambiguation_view()
            elif ans == '6':
                self.add_wiki_data_view()
            elif ans == '7':
                self.add_continent_view()

    def add_continent_view(self):
        continents = ['europe', 'africa', 'america', 'asia', 'australia']
        while True:
            print("%%%%%%%%%%%%%%\n"
                  "add continent\n"
                  "%%%%%%%%%%%%%%\n"
                  "1. add index\n"
                  "2. add continent\n"
                  "e. exit")
            ans = input("value : ")
            if ans == 'e':
                break
            elif ans == '1':
                collection_ans = input("select location collection")
                if collection_ans in self.db.collection_names():
                    locations_collection = self.db[collection_ans]
                    lc.add_index(locations_collection)
                    print("indices added/updated")

            elif ans == '2':
                collection_ans = input("select location collection")
                index = 1
                if collection_ans in self.db.collection_names():
                    locations_collection = self.db[collection_ans]
                    while True:
                        selected_index = input("select index : ")
                        if selected_index == '':
                            index += 1
                        else:
                            index = int(selected_index)
                        location = locations_collection.find_one({'index': index})
                        count = locations_collection.find().count()
                        # doc_continent = location['']
                        print('select continent :\n'
                              'archive name : {}\n'
                              'locations : {}\n'
                              '1 = europe, 2 = africa, 3 = america, 4 = asia, 5 = australia, 6 = other'.format(location['archive_name'], count))
                        continent = int(input("value : "))-1
                        if continent == 5:
                            pass
                        else:
                            try:
                                selected = continents[continent]
                                continent_obj = {
                                    "long_name": selected[0].upper()+selected[1:],
                                    "short_name": selected[0:3],
                                    "types": [
                                        "continent",
                                        "establishment",
                                        "natural_feature"
                                        ]
                                    }
                                existing_doc = locations_collection.find_one({'_id': location['_id'],
                                                                              'geo_data.address_components.types': 'continent'})
                                if existing_doc is None:
                                    location['geo_data'][0]['address_components'].append(continent_obj)
                                    locations_collection.find_one_and_replace({'_id': location['_id']}, location)
                                else:
                                    location['geo_data'][0]['address_components'].pop(-1)
                                    location['geo_data'][0]['address_components'].append(continent_obj)
                                    locations_collection.find_one_and_replace({'_id': location['_id']}, location)

                                print("selected index : {}\n"
                                      "location : {}\n"
                                      "selected continent : {}".format(index, location['archive_name'], selected))

                            except KeyError:
                                print("bad selection")

    def add_wiki_data_view(self):
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
              "        add wiki data\n"
              "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        coll_name = input("select a collection : ")
        documents = self.db[coll_name]
        for doc in documents.find():
            test_all = True
            archive_name = doc['archive_name']
            api_name = doc['geo_data'][0]['formatted_address'].split(', ')[0]
            loc_name_array = [archive_name, api_name]
            wiki_data_in_loc = lc.test_wiki_data(archive_name, doc)
            if wiki_data_in_loc:
                print("wiki data already in location {}".format(archive_name))
            else:
                for loc in loc_name_array:
                    if test_all:
                        wiki_data = lc.add_wiki_data(loc)
                        summary = wiki_data['summary'][0:100]+"..."
                        print("RESULT:\n"
                              "Title tested (arch name) : {}\n"
                              "summary : '{}'".format(loc, summary))
                        ans = input("Confirm y/n : ")
                        if ans == 'n':
                            while True:
                                print("\npropose wiki title :")
                                new_title = input("Value")
                                wiki_data = lc.add_wiki_data(new_title)
                                summary = wiki_data['summary'][0:100] + "..."
                                print("RESULT:\n"
                                      "Title tested (arch name) : {}\n"
                                      "summary : '{}'".format(new_title, summary))
                                ans = input("Confirm y/n : ")
                                if ans == 'n':
                                    pass
                                else:
                                    updated = documents.find_one_and_update({'_id': ObjectId(doc['_id'])},
                                                                            {'$set': {'wiki_data': wiki_data}},
                                                                            return_document=ReturnDocument.AFTER)
                                    print('location {} (id:{}) updated'.format(updated['archive_name'], updated['_id']))
                                    test_all = False
                                    break

                        else:
                            updated = documents.find_one_and_update({'_id': ObjectId(doc['_id'])},
                                                                    {'$set': {'wiki_data': wiki_data}},
                                                                    return_document=ReturnDocument.AFTER)
                            print('location {} (id:{}) updated'.format(updated['archive_name'], updated['_id']))
                            test_all = False
                    else:
                        print("title name {} skipped".format(loc))
                        pass
                """
                wiki_data_doc = documents.find_one({'_id': ObjectId(doc['_id']), 'wiki_data': {'$exists': False}})
                if wiki_data_doc is not None:
                    wiki_empty_obj = {
                        'title': '',
                        'summary': ''
                    }
                    documents.find_one_and_update({'_id': ObjectId(doc['_id'])},
                                                  {'$set': {'wiki_data': wiki_empty_obj}})
                """
    def disambiguation_view(self):
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
              "       country name disambiguation\n"
              "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
              "WARNING: dont forget to backup db\n"
              "1. country name disambiguation\n"
              "2. dump show ids")
        coll_name = input("select a collection : ")
        expr = input("Insert regex : ")
        coll = self.db[coll_name]
        res = lc.get_doc_by_regex(expr, coll)
        documents = res[0]
        count = res[1]
        print("document found : {}\n"
              "expressions : {}\n"
              "1. merge\n"
              "2. pour out\n"
              "e. exit".format(count, [el['archive_name'] for el in documents]))
        decision = input('Value : ')
        if decision == '1':
            res = lc.country_name_disambiguation(documents)
            len_show_ids = [len(doc['show_id']) for doc in res]
            total = reduce(lambda x, y: x+y, len_show_ids)
            print("{} ids per location".format(int(total/len(res))))
            update = input('update ? y/n:')
            if update == 'n':
                pass
            else:
                for doc in res:
                    updated = coll.find_one_and_update({'_id': ObjectId(doc['_id'])},
                                                       {"$set": {'show_id': doc['show_id']}},
                                                       return_document=ReturnDocument.AFTER)
                    print('location {} (id:{}) updated'.format(updated['archive_name'], updated['_id']))

        elif decision == '2':
            to_pour = input('index values ex: 0, 1, 2 etc : ')
            to_pour = [int(ind) for ind in to_pour.split(', ')]
            target = input('target value (index)')
            target = int(target)
            len_target_show_id_before_pour = len(documents[target]['show_id'])
            res = lc.dump_show_ids(documents, to_pour, target)
            target_ids_count = len(res[target]['show_id'])
            print("target location : {}\n"
                  "target ids extended from {} item to {}".format(res[target]['archive_name'],
                                                                  len_target_show_id_before_pour,
                                                                  target_ids_count))
            update = input('Update ? y/n : ')
            if update == 'n':
                pass
            else:
                updated = coll.find_one_and_update({'_id': ObjectId(res[target]['_id'])},
                                                   {"$set": {'show_id': res[target]['show_id']}},
                                                   return_document=ReturnDocument.AFTER)
                print('location {} (id:{}) updated'.format(updated['archive_name'], updated['_id']))
        elif decision == 'e':
            pass

    def add_geo_data_view(self):

        print("WARNING : Select a 'location objects' collection")
        collection_ans = input('Name of the collection : ')

        location_collection = self.db[collection_ans]
        alias_collection = self.db['location_collection']

        for location in self.location_objects:
            alias = ''
            location_name = location["archive_name"]
            in_db = location_collection.find_one({'archive_name': location_name})
            if in_db is None:
                alias_coll_location = alias_collection.find_one({'archive_name': location_name}, {'alias': 1})
                # res = schema.dump(alias_coll_location)
                try:
                    if alias_coll_location['alias'] != location_name:
                        alias = alias_coll_location['alias']
                except TypeError:
                    pass

                res = lc.request_gg_api(location_name)
                try:
                    formatted_address = res[0]['formatted_address']
                except IndexError:
                    formatted_address = 'No value'
                str_res = "\n" \
                          "archive name : {}\n" \
                          "formatted address (res) : {}\n" \
                          "1. validate\n" \
                          "2. try with alias\n" \
                          "s. skip\n" \
                          "e. exit".format(location_name, formatted_address)
                print(str_res)
                ans = input("Value : ")
                if ans == '1' or ans == '':
                    location['geo_data'] = res
                    res = lc.save_data(location, location_collection)
                    print("doc {} added".format(res['_id']))
                    pass
                elif ans == '2':
                    if alias == '':
                        while True:
                            alias_ans = input("\n***************\n"
                                              "new alias : ")
                            res = lc.request_gg_api(alias_ans)
                            formatted_address = res[0]['formatted_address']
                            str_res = "\n" \
                                      "alias tested : {}\n" \
                                      "formatted address : {}\n" \
                                      "1. validate\n" \
                                      "2. try another alias\n" \
                                      "e. exit".format(alias_ans, formatted_address)
                            print(str_res)
                            ans = input("Value : ")
                            if ans == '1':
                                location['geo_data'] = res
                                location['alias'] = alias_ans
                                res = lc.save_data(location, location_collection)
                                print("doc {} added".format(res['_id']))
                                break
                            elif ans == '2':
                                pass
                            elif ans == 'e':
                                break
                    else:
                        print("try suggested alias : {} y/n".format(alias))
                        alias_ans = input('value : ')

                        if alias_ans == 'n':
                            while True:
                                alias_ans = input("\n***************\n"
                                                  "type new alias : ")
                                res = lc.request_gg_api(alias_ans)
                                formatted_address = res[0]['formatted_address']
                                str_res = "\n" \
                                          "alias tested : {}\n" \
                                          "formatted address : {}\n" \
                                          "1. validate\n" \
                                          "2. try another alias\n" \
                                          "e. exit".format(alias_ans, formatted_address)
                                print(str_res)
                                ans = input("Value : ")
                                if ans == '1':
                                    location['geo_data'] = res
                                    location['alias'] = alias_ans
                                    res = lc.save_data(location, location_collection)
                                    print("doc {} added".format(res['_id']))
                                    break
                                elif ans == '2':
                                    pass
                                elif ans == 'e':
                                    break
                        else:
                            retry_alias = alias
                            while True:
                                res = lc.request_gg_api(retry_alias)
                                formatted_address = res[0]['formatted_address']
                                str_res = "\n" \
                                          "alias tested : {}\n" \
                                          "formatted address : {}\n" \
                                          "1. validate\n" \
                                          "2. try with alias\n" \
                                          "e. exit".format(retry_alias, formatted_address)
                                print(str_res)
                                ans = input("Value : ")
                                if ans == '1':
                                    location['geo_data'] = res
                                    location['alias'] = retry_alias
                                    res = lc.save_data(location, location_collection)
                                    print("doc {} added".format(res['_id']))
                                    break
                                elif ans == '2':
                                    retry_ans = input('New alias : ')
                                    retry_alias = retry_ans
                                    pass
                                elif ans == 'e':
                                    break
                elif ans == 'e':
                    break
                elif ans == 's':
                    pass
            else:
                print("skip {}, already in db".format(location_name))

    def prepare_location_object_view(self):

        collection_ans = input('Select a collection : ')
        if collection_ans in self.db.collection_names():
            show_collection = self.db[collection_ans]
            self.location_objects = lc.create_location_object(show_collection)
            print("\n"
                  "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
                  "{} location objects stored\n"
                  "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n".format(len(self.location_objects)))

    def add_missing_values_view(self):

        collection_ans = input('Select a collection : ')
        if collection_ans in self.db.collection_names():

            show_collection = self.db[collection_ans]
            missing_value_count = show_collection.find(
                        {"thematicGeographicalsExtracted": {"$exists": False}}
                    ).count()
            show_collection_count = show_collection.find().count()
            # delta = show_collection_count - missing_value_count

            if missing_value_count > 0:
                manual_op_ans = input('{} document digged\n'
                                      '{} document without geo data\n'
                                      'add geo data manually ? y/n\n'
                                      'Value : '.format(show_collection_count, missing_value_count))
                if manual_op_ans == 'n':
                    pass
                else:
                    location_array = []
                    missing_value_subset = show_collection.find(
                        {"thematicGeographicalsExtracted": {"$exists": False}}
                    )
                    for doc in missing_value_subset:
                        try:
                            summary = doc['alternativeSummary']
                        except KeyError:
                            summary = '-'
                        print("doc title : {}\n"
                              "resume : {}\n".format(doc['title'], summary))
                        location_ans = input('Location ? : ')
                        location_ans = location_ans.split(',')

                        location_array.append({'id': doc['id'], 'extract': location_ans})
                        lc.update_collection(location_array, show_collection)
            else:
                print('\n=> no missing values\n')

    def extract_geo_values_view(self):

        # get sub set where the geo data exists

        collection_ans = input('Select a collection : ')
        if collection_ans in self.db.collection_names():

            show_collection = self.db[collection_ans]
            ans = input("Run extract geo values ? : y/n ")

            if ans == 'y':
                extract = lc.extract_geo_values(show_collection)
                update_ans = input('{} document digged\n'
                                   'update collection ? y/n\n'
                                   'Value: '.format(len(extract)))

                if update_ans == 'n':
                    pass
                else:
                    lc.update_collection(extract, show_collection)

            else:
                print('aborted...')

        else:
            print("the selected collection does not exist\n"
                  "operation aborted...")
