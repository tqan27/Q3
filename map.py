# malaysia_map_app.py
import streamlit as st
import folium
import csv
from streamlit_folium import st_folium

def create_tourist_map():
    # Filepath for the CSV file
    filename = "malaysia_tourist_spots_with_description.csv"

    # Define a color mapping for attraction types
    color_mapping = {
        "Historical Site": "blue",
        "Natural Wonder": "green",
        "Amusement Park": "red",
        "Architectural Landmark": "orange",
        "Others": "gray"
    }

    # Create a map centered around Malaysia
    malaysia_map = folium.Map(location=[4.2105, 101.9758], zoom_start=6)

    # Create FeatureGroups for each attraction type
    feature_groups = {attraction_type: folium.FeatureGroup(name=attraction_type)
                     for attraction_type in color_mapping.keys()}

    # Initialize counter for total attractions
    total_attractions = 0
    # Dictionary to store count by type
    type_counts = {attraction_type: 0 for attraction_type in color_mapping.keys()}

    # Read the tourist spots from the CSV file and add markers
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_attractions += 1
            
            name = row["Tourist Spot"]
            location = row["Location"]
            latitude = float(row["Latitude"])
            longitude = float(row["Longitude"])
            description = row["Description"]
            attraction_type = row["Attraction Type"]
            
            # Update type counter
            if attraction_type in type_counts:
                type_counts[attraction_type] += 1
            else:
                type_counts["Others"] += 1

            # Determine marker color based on attraction type
            color = color_mapping.get(attraction_type, color_mapping["Others"])

            # Add marker to the corresponding FeatureGroup
            folium.Marker(
                [latitude, longitude],
                popup=f"<b>{name}</b><br>{location}<br>{description}",
                tooltip=name,
                icon=folium.Icon(color=color),
            ).add_to(feature_groups.get(attraction_type, feature_groups["Others"]))

    # Add all FeatureGroups to the map
    for feature_group in feature_groups.values():
        feature_group.add_to(malaysia_map)

    # Add a LayerControl to toggle attraction types
    folium.LayerControl().add_to(malaysia_map)

    return malaysia_map, total_attractions, type_counts

def main():
    # Set page config
    st.set_page_config(page_title="Malaysia Tourist Attractions", layout="wide")

    # Add title and description
    st.title("Malaysia Tourist Attractions Map")
    st.write("Explore tourist attractions across Malaysia. Use the layer control to filter by type.")

    # Create two columns
    col1, col2 = st.columns([7, 3])

    # Create and display the map
    malaysia_map, total_attractions, type_counts = create_tourist_map()
    
    with col1:
        # Display the map using streamlit-folium
        st_folium(malaysia_map, width=800, height=600)

    with col2:
        # Display statistics in a sidebar
        st.subheader("Statistics")
        st.metric("Total Attractions", total_attractions)
        
        st.subheader("Attractions by Type")
        for type_, count in type_counts.items():
            if count > 0:
                st.metric(type_, count)

if __name__ == "__main__":
    main()