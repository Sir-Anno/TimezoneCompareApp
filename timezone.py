import threading
import time
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import streamlit as st

# initialize Nominatim API
geolocator = Nominatim(user_agent="Timezone compare")


def get_user_timezone():
    # get the users location by splitting their timezone
    # e.g. "Europe/London" returns "London"
    tz = st.context.timezone
    city_name = tz.split("/")[-1].replace("_", " ")
    return city_name


class Timezone:
    def __init__(self, name):
        self.data = {
            "name": name,
            "timezone": None,
            "timezone_abbreviation": None,
            "local_time": None,
            "local_date": None,
            "utc_offset": None
        }

        # Get the location using geopy
        location = geolocator.geocode(name, exactly_one=True)
        if not location:
            raise ValueError(f"Could not find location for '{name}'")

        obj = TimezoneFinder()
        tz = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        if not tz:
            raise ValueError(f"Could not determine timezone for '{name}'")

        self.data["timezone"] = tz
        self.timezone_obj = pytz.timezone(tz)
        self.update_time()

    def update_time(self):
        local_time = datetime.now(self.timezone_obj)
        self.data["timezone_abbreviation"] = local_time.tzname()
        self.data["local_time"] = local_time.strftime("%H:%M:%S")
        self.data["local_date"] = local_time.strftime("%d.%m.%y")
        self.data["utc_offset"] = local_time.utcoffset().total_seconds() / 3600

    def time_difference(self, other_location):
        return self.data["utc_offset"] - other_location.data["utc_offset"]

    def __repr__(self):
        return f"Location({self.data})"

    def __eq__(self, other):
        if not isinstance(other, Timezone):
            return False
        return self.data["name"] == other.data["name"] and self.data["utc_offset"] == other.data["utc_offset"]

    def __hash__(self):
        return hash((self.data["name"], self.data["utc_offset"]))


class TimeUpdater:
    def __init__(self, locations):
        self.timezones = locations
        self.running = threading.Event()
        self.running.set()
        self.thread = threading.Thread(target=self.update_loop, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.running.clear()
        self.thread.join()

    def update_loop(self):
        while self.running.is_set():
            now = datetime.now()
            time_to_next_second = 1 - (now.microsecond / 1_000_000)
            time.sleep(time_to_next_second)

            for timezone in self.timezones:
                timezone.update_time()
