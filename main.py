import streamlit as st
from sidebar import sidebar
from add_location import add_location_dialog
import timezone
from timezone import TimeUpdater

st.set_page_config(
    page_title="Timezone compare",
    page_icon="",
    layout="centered",
)

st.title("Timezone compare", anchor=False)
sidebar()

# set up local time
if not "user_local_time" in st.session_state:
    user_local_time = timezone.get_user_timezone()  # get user local time
    user_local_time = timezone.Timezone(user_local_time)  # convert to Timezone object
    st.session_state["user_local_time"] = user_local_time

# setup timezones set
if "timezones" not in st.session_state:
    st.session_state["timezones"] = set()
    st.session_state["timezones"].add(st.session_state["user_local_time"])


@st.fragment(run_every="1s")
def update_ui():
    # convert timezones set to list
    timezones_list = list(st.session_state["timezones"])
    # sort by time difference from the user_local_time
    timezones_list = sorted(
        timezones_list,
        key=lambda tz: tz.time_difference(st.session_state["user_local_time"])
    )

    for time in timezones_list:
        with st.container(border=True):
            name_col, time_col, date_col, abbreviation_col, utc_col, remove_col = st.columns([2, 1, 1, .5, 1, .5],
                                                                                             vertical_alignment="center")

            with name_col:
                st.subheader(time.data["name"], anchor=False)
                time_diff = time.time_difference(st.session_state["user_local_time"])
                if time_diff == 0.0:
                    st.caption("Local time")
                elif time_diff < 0:
                    st.caption(f"{time_diff} hrs behind")
                else:
                    st.caption(f"{time_diff} hrs ahead")

            with time_col:
                st.text(time.data["local_time"])

            with date_col:
                st.text(time.data["local_date"])

            with abbreviation_col:
                st.text(time.data["timezone_abbreviation"])

            with utc_col:
                if time.data["utc_offset"] > 0:
                    st.text(f"UTC +{time.data["utc_offset"]}")
                else:
                    st.text(f"UTC {time.data["utc_offset"]}")

            with remove_col:
                if time != st.session_state["user_local_time"]:
                    st.button("", type="tertiary", icon=":material/cancel:", key=f"cancel_btn_{time}",
                              on_click=lambda: st.session_state["timezones"].remove(time))


with st.container(border=False):
    update_ui()

st.button("Add location", icon="🗺", on_click=add_location_dialog, type="primary", use_container_width=True)

# update times
updater = TimeUpdater(st.session_state["timezones"])
updater.start()
