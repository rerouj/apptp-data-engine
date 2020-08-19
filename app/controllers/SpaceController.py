from schemas.SpaceSchema import *
from bson import ObjectId
import matplotlib.pyplot as plt
import math


class SpaceController(object):

    """Create Object pipeline"""

    class_name = "Create Data Object !"

    # def __init__(self, collections_available):

    #     self.collections_available = collections_available
    #     self.show_id = str()
    #     self.show_title = str()
    #     self.location_array = list()
    #     self.object_collection = list()

    @staticmethod
    def add_continent(obj, collection):
        continent = []
        try:
            continent = [collection.find_one({'archive_name': location_name})['geodata']['context_extended'][-1]['continent'] for location_name in obj.locations_name]
            continent = list(set(continent))
        except TypeError or KeyError:
            print("Archive name {}, id {}".format(obj.locations_name, obj._id))
        return continent

    @staticmethod
    def add_locality_country_space(space, collection):
        locality_space = [loc for loc in space
                          if collection.find_one(
                                {
                                    '_id': loc['location']
                                }
                            )['geo_data'][0]['address_components'][0]['types'][0] == 'locality']
        country_space = [loc for loc in space
                         if collection.find_one(
                                {
                                    '_id': loc['location']
                                }
                            )['geo_data'][0]['address_components'][0]['types'][0] == 'country']
        region_space = [loc for loc in space
                        if collection.find_one(
                                {
                                    '_id': loc['location']
                                }
                            )['geo_data'][0]['address_components'][0]['types'][0] == 'administrative_area_level_1' or
                        collection.find_one(
                                {
                                    '_id': loc['location']
                                }
                            )['geo_data'][0]['address_components'][0]['types'][0] == 'administrative_area_level_2']
        return locality_space, country_space, region_space

    @staticmethod
    def get_location_array(show_id, loc_collection, shows_collection):

        """
        compose and return locations arrary for the selected show
        :returns: Location _id's Dict Array
        """

        location_array = []
        tmp_object = {'location': ''}
        show = shows_collection.find_one({"_id": show_id})
        try:
            location_extracted = show['thematicGeographicalsExtracted']
            if len(location_extracted) > 0:
                for location in location_extracted:
                    tmp_location = loc_collection.find_one({"archive_name": location})
                    try:
                        if {'location': tmp_location["_id"]} not in location_array:
                            tmp_object['location'] = tmp_location["_id"]
                            location_array.append({'location': tmp_location['_id']})
                    except TypeError:
                        pass
                return location_array
        except KeyError:
            pass

    def create_space(self):
        """
        serialise Space() object with Marshmallow
        :return: Space() object
        """
        schema = SpaceSchema()
        data = {'show': str(self.show_id), 'show_title': self.show_title, 'space': self.location_array}
        space_object = schema.load(data)
        return space_object

    @staticmethod
    def plot_coordinates(self, obj, location_collection):

        x = [location_collection.find_one({"_id": ObjectId(_id)}, {"_id": 0, "geodata": 1})["geodata"]['latitude'] for
             _id in obj.get_space()]
        y = [location_collection.find_one({"_id": ObjectId(_id)}, {"_id": 0, "geodata": 1})["geodata"]['longitude'] for
             _id in obj.get_space()]
        location_names = [
            location_collection.find_one({"_id": ObjectId(_id)}, {"_id": 0, "archive_name": 1})['archive_name'] for _id
            in obj.get_space()]
        location_tupple = [(y[ind], x[ind], i) for ind, i in enumerate(location_names)]
        # Plot
        plt.scatter(y, x, alpha=0.5)
        for tup in location_tupple:
            plt.text(tup[0], tup[1], tup[2])
        plt.title(obj.show_title)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show(block=False)
        plt.ion()
        plt.show()
        plt.pause(0.001)
        input("close window ? : ")
        plt.close()

    @staticmethod
    def distance(space, locations):

        """
        sum linear distance between the coordinates
        dist formula : sqrt((xb - xa)**2 + (yb - ya)**2)
        """

        country_linear_distance = 0
        city_linear_distance = 0

        coordinates_array = [(locations.find_one({"_id": dict['location']},
                                                 {"_id": 0, "geo_data": 1})['geo_data'][0]['geometry']['location']['lng'],
                              locations.find_one({"_id": dict['location']},
                                                 {"_id": 0, "geo_data": 1})['geo_data'][0]['geometry']['location']['lat']) for dict in space if locations.find_one({"_id": dict['location']})['geo_data'][0]['address_components'][0]['types'][0] == 'country']

        len_coordinates_array = len(coordinates_array)
        coord_combination = [(val, val+1) for val in range(len_coordinates_array-1)]
        coord_combination = [(coordinates_array[tup[0]], coordinates_array[tup[1]]) for tup in coord_combination]

        for tup in coord_combination:

            term_left = (tup[1][1]-tup[0][1])**2
            term_right = (tup[1][0]-tup[0][0])**2
            dist = math.sqrt(term_left + term_right)
            country_linear_distance += dist

        # we repeat the operation but for city

        coordinates_array = [(locations.find_one({"_id": dict['location']},
                                                 {"_id": 0, "geo_data": 1})['geo_data'][0]['geometry']['location'][
                                  'lng'],
                              locations.find_one({"_id": dict['location']},
                                                 {"_id": 0, "geo_data": 1})['geo_data'][0]['geometry']['location'][
                                  'lat']) for dict in space if
                             locations.find_one({"_id": dict['location']})['geo_data'][0]['address_components'][0][
                                 'types'][0] == 'locality']

        len_coordinates_array = len(coordinates_array)
        coord_combination = [(val, val + 1) for val in range(len_coordinates_array - 1)]
        coord_combination = [(coordinates_array[tup[0]], coordinates_array[tup[1]]) for tup in coord_combination]

        for tup in coord_combination:
            term_left = (tup[1][1] - tup[0][1]) ** 2
            term_right = (tup[1][0] - tup[0][0]) ** 2
            dist = math.sqrt(term_left + term_right)
            city_linear_distance += dist

        country_line_to_km = country_linear_distance * 111
        city_line_to_km = city_linear_distance * 111

        return {'country_coord_dist': country_linear_distance,
                'km_btw_country': country_line_to_km,
                'city_coord_dist': city_linear_distance,
                'city_km_dist': city_line_to_km}

    @staticmethod
    def locations_name_array(space_array, locations):
        """ append locations name's to a Space object"""
        locations_array = [locations.find_one({"_id": dic['location']}, {"_id": 0, "archive_name": 1})["archive_name"] for dic in space_array]
        return locations_array

    @staticmethod
    def serialize_object(self, obj):
        schema = SpaceSchema()
        result = schema.dump(obj)
        return result


"""
    def pipeline(self):
        while True:
            print(self.welcome_text)
            ans = input("Value : ")
            if ans == 'e':
                break
            elif ans == '3':
                obj = self.object_collection[543]
                self.add_locality_space(obj, self.collections_available['locations'])
            elif ans == '2':
                object_number = input("object number : ")
                try:
                    space_selected = self.object_collection[int(object_number)]
                    print("")
                    print(space_selected)
                    print(self.serialize_object(space_selected))
                    self.plot_coordinates(space_selected, self.collections_available['locations'])

                except IndexError:
                    print("no object in store")
            elif ans == '1':
                self.object_collection = []
                print("wait...")
                shows = self.collections_available['shows'].find()
                for show in shows:
                    show_id = show['_id']
                    self.show_id = show_id
                    self.show_title = self.collections_available['shows'].find_one({"_id": self.show_id})["title"]
                    self.get_location_array(self.collections_available['locations'],
                                            self.collections_available['shows'])

                    space_object = self.create_space()

                    self.distance(space_object, space_object.get_space(),
                                  self.collections_available['locations'])
                    self.locations_name_array(space_object, self.collections_available['locations'])
                    if len(space_object.get_space()) > 0:
                        self.object_collection.append(space_object)


                print(len(self.object_collection))
"""""
