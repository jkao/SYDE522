from base_cleaner import BaseCleaner


class ZillowCleaner(BaseCleaner):
    def __init__(
            self,
            data_path,
            broker_labeller_path,
            property_labeller_path):
        BaseCleaner.__init__(
            self, data_path, broker_labeller_path, property_labeller_path)

    def normalize_lat_long(self, entity):
        entity["latitude"] = float(entity["latitude"]) / 10**6
        entity["longitude"] = float(entity["longitude"]) / 10**6

    def normalize_property_type(self, entity):
        entity["propertyType"] = self.label_property("UNK_HOME")

    def normalize_attributes(self, entity):
        BaseCleaner.normalize_attributes(self, entity)
        self.normalize_lat_long(entity)
        self.normalize_property_type(entity)
        return entity

    def clean_entity(self, entity):
        new_entity = self.filter_attributes(entity)
        return self.normalize_attributes(new_entity)

    def clean_data(self):
        cleaned_data = \
            [self.clean_entity(e)
                for e in self.data if self.is_valid_entity(e)]
        return cleaned_data

