import streamlit as st
import timezone


@st.dialog("Add location dialog")
def add_location_dialog():
    timezone_name = st.text_input("Add location", placeholder="Add location",
                                  label_visibility="collapsed").title()

    st.session_state["error message"] = ""

    # add, cancel buttons
    add_col, cancel_col = st.columns(2)
    with add_col:
        if st.button("Add location", use_container_width=True, type="primary"):

            # try to add location
            try:
                # check location name isn't empty
                timezone_name = timezone_name.strip()
                if not timezone_name:
                    st.session_state["error message"] = f"Please enter a location"
                    raise ValueError("Please enter a location")

                new_timezone = timezone.Timezone(timezone_name)
                st.session_state["timezones"].add(new_timezone)
                st.rerun()  # closes dialog

            # couldn't find timezone
            except Exception as e:
                st.session_state["error message"] = f"oops, could not add location: \n{e}"

    with cancel_col:
        if st.button("Cancel", use_container_width=True):
            st.rerun()  # closes dialog

    # error message
    st.text(st.session_state["error message"])
