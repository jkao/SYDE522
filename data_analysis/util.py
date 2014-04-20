from sklearn import preprocessing

import json
import numpy as np

class Util(object):
    @staticmethod
    def load_json_to_numpy_array(path):
        ordered_props = [
                "bathrooms",
                "bedrooms",
                "broker",
                "latitude",
                "longitude",
                "photoCount",
                "propertySize",
                "propertyType"
                ]

        with open(path, "r") as f:
            json_data = json.load(f)

        x_array = []
        y_array = []
        for j in json_data:
            entity = []
            for field in ordered_props:
                entity.append(j[field])
            x_array.append(entity)
            y_array.append(j["price"])

        return (np.array(x_array), np.array(y_array))
