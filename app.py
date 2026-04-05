import streamlit as st
import pandas as pd
import math
import time
from streamlit_js_eval import get_geolocation

# --- 1. GEOSPATIAL LOGIC (Haversine Formula) ---
def calculate_distance(lat1, lon1, lat2, lon2):
    radius = 6371  # Earth radius in km
    dlat, dlon = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return radius * c

# --- 2. DATABASE INITIALIZATION ---
if 'donors' not in st.session_state:
    st.session_state.donors = [
        {"id": 1, "name": "Arjun", "blood": "O+", "phone": "9988776655", "lat": 17.440, "lon": 78.340},
        {"id": 2, "name": "Priya", "blood": "O-", "phone": "9844332211", "lat": 17.455, "lon": 78.355},
        {"id": 3, "name": "Rahul", "blood": "A+", "phone": "9123456789", "lat": 17.460, "lon": 78.360},
        {"id": 4, "name": "Sita", "blood": "B+", "phone": "9000011111", "lat": 17.430, "lon": 78.330},
        {"id": 5, "name": "Kiran", "blood": "A+", "phone": "9222233333", "lat": 17.445, "lon": 78.342},
        {"id": 6, "name": "Sneha", "blood": "O+", "phone": "9333344444", "lat": 17.442, "lon": 78.335},
    ]

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="Smart Blood Finder", layout="wide", page_icon="🩸")
st.title("🩸 Smart Blood Donor Finder")
st.markdown("---")

# Sidebar
st.sidebar.header("🔍 Search Filters")

selected_groups = st.sidebar.multiselect(
    "Select Required Blood Groups",
    ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"],
    default=["O+"]
)

max_dist = st.sidebar.slider("Search Radius (km)", 1, 20, 5)

# Seeker location (fixed)
seeker_lat, seeker_lon = 17.448, 78.348

# --- 4. FILTERING ---
nearby_donors = []

for d in st.session_state.donors:
    dist = calculate_distance(seeker_lat, seeker_lon, d['lat'], d['lon'])

    if d['blood'] in selected_groups and dist <= max_dist:
        d_copy = d.copy()
        d_copy['distance'] = round(dist, 2)
        nearby_donors.append(d_copy)

nearby_donors.sort(key=lambda x: x['distance'])

# --- 5. DASHBOARD ---
col1, col2 = st.columns([2, 1])

# LEFT SIDE
with col1:
    st.subheader(f"Results for: {', '.join(selected_groups)}")

    if nearby_donors:
        display_df = pd.DataFrame(nearby_donors)[['name', 'blood', 'distance']]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.write("**Map View of Nearby Donors**")
        map_df = pd.DataFrame(nearby_donors)
        st.map(map_df)
    else:
        st.warning("No donors found in this range.")

# RIGHT SIDE
with col2:
    st.subheader("Action Center")

    if nearby_donors:
        target_label = st.selectbox(
            "Select a Donor to Request",
            [f"{d['name']} ({d['blood']}) - {d['distance']} km" for d in nearby_donors]
        )

        if st.button("Ping Donor", use_container_width=True):
            with st.spinner("Sending Request..."):
                time.sleep(1)
                st.session_state.pinged = True
                st.info(f"Ping sent to {target_label}!")

        # WAITING STATE
        if st.session_state.get('pinged'):
            st.markdown("---")
            st.write("⏳ Waiting for Donor response...")

            if st.button("Simulate Donor: ACCEPT", type="primary"):
                st.session_state.accepted = True

        # ACCEPTED STATE
        if st.session_state.get('accepted'):
            st.success("✅ Donor has Accepted!")

            donor_name = target_label.split(" (")[0]
            donor_info = next(d for d in nearby_donors if d['name'] == donor_name)

            st.markdown(f"""
            ### Contact Details:
            - **Name:** {donor_info['name']}
            - **Blood:** {donor_info['blood']}
            - **Phone:** **{donor_info['phone']}**
            """)

            st.button("📞 Call Now", use_container_width=True)

            # --- GPS TRACKING SECTION ---
            st.markdown("---")
            st.subheader("📍 Live GPS Tracking")

            location = get_geolocation()

            if location:
                lat = location['coords']['latitude']
                lon = location['coords']['longitude']

                st.success("Live Location Captured!")

                st.write(f"Latitude: {lat}")
                st.write(f"Longitude: {lon}")

                gps_df = pd.DataFrame({
                    'lat': [lat],
                    'lon': [lon]
                })

                st.map(gps_df)

            else:
                st.warning("⚠️ Please allow location access in your browser.")

    else:
        st.info("Adjust filters to see donors.")

st.markdown("---")
st.caption("Built for Real-time Blood Emergency Management") 