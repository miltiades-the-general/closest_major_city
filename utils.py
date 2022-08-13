import math
import numpy as np
import heapq
from dotenv import load_dotenv
import os
import requests
import heapq

class GeoUtilities():
    R = 3963
    sin = math.sin
    cos = math.cos
    atan2 = math.atan2
    sqrt = np.sqrt
    rad = math.radians
    def __init__(self, latitude: list, longitude: list):
        self.latitude = latitude
        self.longitude = longitude
        


    def find_distance(self):
        sin = self.sin
        cos = self.cos
        rad = self.rad
        atan2 = self.atan2
        sqrt = self.sqrt
        lng1 = self.longitude[0] 
        lng2 = self.longitude[1]
        lat1 = self.latitude[0]
        lat2 = self.latitude[1]

        dlat = rad(lat2-lat1)
        dlng = rad(lng2-lng1)


        a = sin(dlat/2) * sin(dlat/2) + cos(rad(lat1)) * cos(rad(lat2)) * sin(dlng/2) * sin(dlng/2)
        c = 2 * atan2((sqrt(a)), (sqrt(1-a)))
        d = self.R * c

        return d

    
class FindClosestCity:
    # def __init__(self):
    def find_closest_city(data):
        # self.data = data
        closest_city_index = 0

        for index, curr_city in enumerate(data):
            min_distance = 12500
            lat1 = curr_city['latitude']
            lng1 = curr_city['longitude']
            for pointer, city in enumerate(data):
                if pointer == index:
                    pass
                else:
                    lat2 = city['latitude']
                    lng2 = city['longitude']
                    distance = GeoUtilities([lat1, lat2], [lng1, lng2]).find_distance()
                    if distance < min_distance:
                        closest_city_index = pointer
                    min_distance = min(min_distance, distance)
            data[index]['closestCity'] = {'name': data[closest_city_index]['name'], 'region': data[closest_city_index]['region'], 'distance': min_distance}
        return data

    def find_closest_city_to_point(data, city_name, state_code):
        load_dotenv()

        API_key = os.getenv("OPEN-WEATHER-API-KEY")
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},US&limit=1&appid={API_key}"

        fetch = requests.get(
            url,
        ).json()[0]

        lat1 = fetch['lat']
        lng1 = fetch['lon']
        min_distance = 12500

        for index, city in enumerate(data):
            lat2 = city['latitude']
            lng2 = city['longitude']
            distance = GeoUtilities([lat1, lat2], [lng1, lng2]).find_distance()
            if distance < min_distance:
                closest_city_index = index
            min_distance = min(min_distance, distance)
        return f"Closest City: {data[closest_city_index]['name']}, distance: {min_distance: .02f} miles"


    def find_two_closest_cities_to_point(data, city_name, state_code):
        pushpop = heapq.heappushpop
        load_dotenv()

        API_key = os.getenv("OPEN-WEATHER-API-KEY")
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},US&limit=1&appid={API_key}"

        fetch = requests.get(
            url,
        ).json()[0]

        lat1 = fetch['lat']
        lng1 = fetch['lon']
        min_distance = [-12500, -12500]
        heapq.heapify(min_distance)
        closest_city_index = ["city2", "city1"]

        for index, city in enumerate(data):
            lat2 = city['latitude']
            lng2 = city['longitude']
            distance = -GeoUtilities([lat1, lat2], [lng1, lng2]).find_distance()
            if distance > min_distance[0] and distance < min_distance[1]:
                pushpop(min_distance, distance)
                closest_city_index[0] = index
            elif distance > min_distance[1]:
                pushpop(min_distance, distance)
                closest_city_index[0] = closest_city_index[1]
                closest_city_index[1] = index
            
        
        
        closest_city = data[closest_city_index[1]]["name"]
        closest_state = data[closest_city_index[1]]["region"]
        second_closest_city = data[closest_city_index[0]]["name"]
        second_closest_state= data[closest_city_index[0]]["region"]

        # print(f"closest: {closest_city}, second: {second_closest_city}")

        if city_name == closest_city:
            return f"Closest City: {second_closest_city}, {second_closest_state}, distance: {-min_distance[0]: .02f} miles"
        
        else:
            return f"Closest City: {closest_city}, {closest_state}, distance: {-min_distance[1]: .02f} miles"


      
      

                    
                  