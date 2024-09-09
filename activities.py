import pandas as pd

class Activities:
    def __init__(self, data):
        if isinstance(data, pd.DataFrame):
            self._data = data
        else:
            self._data = pd.DataFrame(data)

        self._units = "m"

    @property
    def data(self):
        return self._data
    
    @property
    def cols(self):
        return self._data.columns

    @property
    def units(self):
        return self._units
    
    def mod_activities(self, sport_type=None, workout_type=None, units=None):
        mod_data = self.data

        # filter activities
        if sport_type:
            mod_data = mod_data[mod_data["sport_type"] ==
                                           sport_type].reset_index(drop=True)

        if workout_type:
            mod_data = mod_data[mod_data["workout_type"] ==
                                           workout_type].reset_index(drop=True)
            
        # modify units
        if units:
            if units == "km":
                mod_data["distance"] = mod_data["distance"].apply(
                    lambda dist: (dist / 1000))
                self._units = "km"
            if units == "miles":
                mod_data["distance"] = mod_data["distance"].apply(
                    lambda dist: (dist * 0.000621371))
                self._units = "miles"
            
        return mod_data
    