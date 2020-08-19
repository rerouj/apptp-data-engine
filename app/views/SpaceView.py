from globals import *
from controllers.SpaceController import SpaceController as Sc
from schemas.SpaceSchema import SpaceSchema
from classes import Space as Sp


class SpaceView:

    """Space module view class"""

    def __init__(self, db):
        self.object_collection = []
        self.db = db

    def home_view(self):
        while True:
            print(SPACE_VIEW_WELCOME_STR)
            ans = input("value: ")
            if ans == '1':
                self.create_space_objects_view()
                print('process ended')
            if ans == '2':
                self.add_locality_space_view()
                print('process ended')
            if ans == '3':
                save = input('save objects ? y/n')
                if save == 'n':
                    pass
                else:
                    documents_array = []
                    collection_name = input('name a collection to save your data')
                    print("collection : {}".format(collection_name))
                    ans = input("confirm y/n")
                    if ans == 'n':
                        pass
                    else:
                        collection = self.db[collection_name]
                        for obj in self.object_collection:
                            schema = SpaceSchema()
                            res = schema.dump(obj)
                            documents_array.append(res)
                        collection.insert_many(documents_array)
                        print("SUCCESS :\n"
                              "{} document inserted".format(len(documents_array)))

            if ans == '4':
                self.add_continent_view()
            if ans == 'e':
                break

    def add_continent_view(self):
        locations = self.db['location_collection']
        for obj in self.object_collection:
            obj.continent_space = Sc.add_continent(obj, locations)
            print(obj.continent_space)

    def add_locality_space_view(self):
        """
        extract locality location and produce the corresponding array
        :returns: locality ids array
        """
        locations = self.db['locations']
        for obj in self.object_collection:
            res = Sc.add_locality_country_space(obj.space, locations)
            obj.locality_space = res[0]
            obj.country_space = res[1]
            obj.region_space = res[2]
        print("locality & country space added to each object")

    def create_space_objects_view(self):

        empty_objects = 0

        show_coll_name = input("Select a show collection : ")
        locations_coll_name = input("Select a location collection :")
        if show_coll_name in self.db.collection_names():
            show_collection = self.db[show_coll_name]
            if locations_coll_name in self.db.collection_names():
                location_collection = self.db[locations_coll_name]
                print("wait...")
                for show in show_collection.find():

                    show_id = show['_id']
                    show_title = show["title"]
                    locations_array = Sc.get_location_array(show['_id'], location_collection, show_collection)
                    space_obj = Sp.Space(show_id, show_title, locations_array)

                    distance = Sc.distance(space_obj.space, location_collection)
                    space_obj.distance = distance
                    locations_name_array = Sc.locations_name_array(space_obj.space, location_collection)
                    space_obj.locations_name = locations_name_array
                    if len(space_obj.space) > 0:
                        self.object_collection.append(space_obj)
                    else:
                        empty_objects += 1
                print("{} object created, {} empty show rejected".format(len(self.object_collection), empty_objects))
