
#new

import pymysql
import streamlit as st
import pandas as pd

# Database connection setup
con = pymysql.connect(
    host="localhost",
    user="root",
    password="Omsairam_10",
    database="Redbus_project_new",
    autocommit=True
)
mycursor = con.cursor()

# Function to fetch data 
def get_data(query, filter_data=()):
    mycursor.execute(query, filter_data)
    data = mycursor.fetchall()
    column_names = [desc[0] for desc in mycursor.description]
    return pd.DataFrame(data, columns=column_names)

# Streamlit app
def main():
    st.title("[*red* Bus]")
    logo = "H:/IIT-M GUVI/Projects/Screenshot 2024-07-30 102903.png"
    caption_image = "H:/IIT-M GUVI/Projects/Screenshot 2024-07-30 102941.png"
    st.header("India's No. 1 Online Bus Ticket Booking Site", divider="gray")
    st.image(caption_image)
    st.sidebar.image(logo, caption='Travel company', use_column_width=True)

    state = st.sidebar.selectbox("Select the state:", ("APSRTC", "KSRTC", "TSRTC", "WB", "KTCL", "Punjab", "BSRTC", "RSRTC", "J&K", "Chandigarh"))

    # Define table name based on the selected state
    table_name = {
        "APSRTC": "apsrtc_bus_details",
        "KSRTC": "ksrtc_bus_details",
        "TSRTC": "tsrtc_bus_details",
        "BSRTC": "bihar_bus_details",
        "WB": "wb_bus_details",
        "KTCL": "ktcl_bus_details",
        "Punjab": "punjab_bus_details",
        "RSRTC": "rsrtc_bus_details",
        "J&K": "jk_bus_details",
        "Chandigarh": "chandigarh_bus_details"
    }.get(state)

    st.subheader(f"{state} State Road Transport Corporation", divider="red")

    # Fetch and display data
    query = f"SELECT * FROM {table_name}"
    df = get_data(query)
    st.dataframe(df)

    # Add filtering options
    st.sidebar.header('Filter Options')
    routes = df['Route_name'].unique() if 'Route_name' in df.columns else []
    route = st.sidebar.selectbox("Select route", list(routes))
    
    min_price = st.sidebar.number_input("Minimum price:", min_value=0, value=0)
    max_price = st.sidebar.number_input("Maximum price:", min_value=0, value=1000)
    min_rating = st.sidebar.number_input("Minimum rating:", min_value=0.0, max_value=5.0, value=0.0)
    max_rating = st.sidebar.number_input("Maximum rating:", min_value=0.0, max_value=5.0, value=5.0)

    # Build the query with filters
    conditions = []
    filter_data = []
    
    if route != 'All':
        conditions.append("Route_name = %s")
        filter_data.append(route)
    if min_price is not None:
        conditions.append("Price >= %s")
        filter_data.append(min_price)
    if max_price is not None:
        conditions.append("Price <= %s")
        filter_data.append(max_price)
    if min_rating is not None:
        conditions.append("Rating >= %s")
        filter_data.append(min_rating)
    if max_rating is not None:
        conditions.append("Rating <= %s")
        filter_data.append(max_rating)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Fetch and display filtered data
    filtered_df = get_data(query, tuple(filter_data))
    if not filtered_df.empty:
        st.dataframe(filtered_df)
    else:
        st.write("No data found for the given filters.")

if __name__ == "__main__":
    main()
