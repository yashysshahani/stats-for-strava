import pandas as pd
import streamlit as st

class Activities:
    def __init__(self, data, units="Meters"):
        if isinstance(data, pd.DataFrame):
            self._data = data
        else:
            self._data = pd.DataFrame(data)

        self._units = units

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
            if units == "Kilometers":
                mod_data["distance"] = mod_data["distance"].apply(
                    lambda dist: (dist / 1000))
                self._units = "Kilometers"
            if units == "Miles":
                mod_data["distance"] = mod_data["distance"].apply(
                    lambda dist: (dist * 0.000621371))
                self._units = "Miles"
                
            
        return mod_data
    