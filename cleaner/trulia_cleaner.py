from base_cleaner import BaseCleaner


class TruliaCleaner(BaseCleaner):
    def __init__(
            self,
            data_path,
            broker_labeller_path,
            property_labeller_path):
        BaseCleaner.__init__(
            self, data_path, broker_labeller_path, property_labeller_path)

    def normalize_lat_long(self, entity):
        entity["latitude"] = float(entity["latitude"])
        entity["longitude"] = float(entity["longitude"])

    def normalize_property_type(self, entity):
        if entity["propertyType"]:
            entity["propertyType"] = \
                self.label_property(entity["propertyType"])
        else:
            entity["propertyType"] = \
                self.label_property("UNK_HOME")

    def normalize_attributes(self, entity):
        BaseCleaner.normalize_attributes(self, entity)
        self.normalize_lat_long(entity)
        self.normalize_property_type(entity)
        return entity

    def clean_entity(self, entity):
        new_entity = self.filter_attributes(entity)
        return self.normalize_attributes(new_entity)

    def is_valid_entity(self, entity):
        if BaseCleaner.is_valid_entity(self, entity):
            if entity["bathrooms"] \
                and entity["longitude"] \
                and entity["latitude"] \
                and entity["propertySize"]:
                return True
            else:
                return False
        else:
            return False

    def clean_data(self):
        cleaned_data = \
            [self.clean_entity(e)
                for e in self.data if self.is_valid_entity(e)]
        return cleaned_data

