# %% [markdown]
# ## Oil Shipping Network Visualization with Edge Bundling <br>

# Simulates global oil tanker traffic between major oil ports/regions. <br>
# Demonstrates edge weight functionality where heavier shipping routes <br>
# %%
import numpy as np
import pandas as pd
import igraph as ig
from ggplotly import ggplot, aes, geom_edgebundle, geom_map, theme_dark, labs

# Set seed for reproducibility
np.random.seed(42)

# %%
# =============================================================================
# Define number of edges
# =============================================================================

n_edges = 10000

# %%
# =============================================================================
# Define major oil ports/terminals (200 nodes)
# =============================================================================


ports = pd.DataFrame([
    # Middle East - Major exporters
    {"name": "Ras Tanura", "lon": 50.03, "lat": 26.64, "region": "Middle East", "type": "export"},
    {"name": "Kharg Island", "lon": 50.32, "lat": 29.23, "region": "Middle East", "type": "export"},
    {"name": "Fujairah", "lon": 56.33, "lat": 25.12, "region": "Middle East", "type": "export"},
    {"name": "Jebel Ali", "lon": 55.03, "lat": 24.98, "region": "Middle East", "type": "export"},
    {"name": "Basra", "lon": 47.78, "lat": 30.51, "region": "Middle East", "type": "export"},
    {"name": "Kuwait City", "lon": 47.98, "lat": 29.38, "region": "Middle East", "type": "export"},
    {"name": "Yanbu", "lon": 38.06, "lat": 24.09, "region": "Middle East", "type": "export"},
    {"name": "Muscat", "lon": 58.54, "lat": 23.61, "region": "Middle East", "type": "export"},

    # Asia - Major importers
    {"name": "Singapore", "lon": 103.85, "lat": 1.29, "region": "Asia", "type": "hub"},
    {"name": "Shanghai", "lon": 121.47, "lat": 31.23, "region": "Asia", "type": "import"},
    {"name": "Ningbo", "lon": 121.55, "lat": 29.87, "region": "Asia", "type": "import"},
    {"name": "Qingdao", "lon": 120.38, "lat": 36.07, "region": "Asia", "type": "import"},
    {"name": "Busan", "lon": 129.03, "lat": 35.10, "region": "Asia", "type": "import"},
    {"name": "Yokohama", "lon": 139.64, "lat": 35.44, "region": "Asia", "type": "import"},
    {"name": "Chiba", "lon": 140.10, "lat": 35.61, "region": "Asia", "type": "import"},
    {"name": "Kaohsiung", "lon": 120.27, "lat": 22.62, "region": "Asia", "type": "import"},
    {"name": "Hong Kong", "lon": 114.17, "lat": 22.32, "region": "Asia", "type": "hub"},
    {"name": "Mumbai", "lon": 72.88, "lat": 19.08, "region": "Asia", "type": "import"},
    {"name": "Chennai", "lon": 80.27, "lat": 13.08, "region": "Asia", "type": "import"},
    {"name": "Visakhapatnam", "lon": 83.30, "lat": 17.69, "region": "Asia", "type": "import"},

    # Europe - Importers and refineries
    {"name": "Rotterdam", "lon": 4.48, "lat": 51.92, "region": "Europe", "type": "hub"},
    {"name": "Antwerp", "lon": 4.40, "lat": 51.22, "region": "Europe", "type": "import"},
    {"name": "Hamburg", "lon": 9.99, "lat": 53.55, "region": "Europe", "type": "import"},
    {"name": "Le Havre", "lon": 0.11, "lat": 49.49, "region": "Europe", "type": "import"},
    {"name": "Marseille", "lon": 5.37, "lat": 43.30, "region": "Europe", "type": "import"},
    {"name": "Genoa", "lon": 8.93, "lat": 44.41, "region": "Europe", "type": "import"},
    {"name": "Trieste", "lon": 13.77, "lat": 45.65, "region": "Europe", "type": "import"},
    {"name": "Algeciras", "lon": -5.45, "lat": 36.13, "region": "Europe", "type": "hub"},
    {"name": "Sines", "lon": -8.87, "lat": 37.95, "region": "Europe", "type": "import"},
    {"name": "Milford Haven", "lon": -5.05, "lat": 51.71, "region": "Europe", "type": "import"},

    # Africa - Exporters
    {"name": "Bonny", "lon": 7.17, "lat": 4.43, "region": "Africa", "type": "export"},
    {"name": "Lagos", "lon": 3.39, "lat": 6.45, "region": "Africa", "type": "export"},
    {"name": "Luanda", "lon": 13.23, "lat": -8.84, "region": "Africa", "type": "export"},
    {"name": "Pointe-Noire", "lon": 11.86, "lat": -4.77, "region": "Africa", "type": "export"},
    {"name": "Durban", "lon": 31.03, "lat": -29.86, "region": "Africa", "type": "import"},
    {"name": "Alexandria", "lon": 29.92, "lat": 31.20, "region": "Africa", "type": "hub"},
    {"name": "Suez", "lon": 32.55, "lat": 29.97, "region": "Africa", "type": "hub"},

    # Americas - Mixed
    {"name": "Houston", "lon": -95.36, "lat": 29.76, "region": "Americas", "type": "hub"},
    {"name": "Louisiana Offshore", "lon": -90.00, "lat": 28.50, "region": "Americas", "type": "export"},
    {"name": "Corpus Christi", "lon": -97.40, "lat": 27.80, "region": "Americas", "type": "export"},
    {"name": "New York", "lon": -74.01, "lat": 40.71, "region": "Americas", "type": "import"},
    {"name": "Philadelphia", "lon": -75.16, "lat": 39.95, "region": "Americas", "type": "import"},
    {"name": "Cartagena", "lon": -75.51, "lat": 10.39, "region": "Americas", "type": "export"},
    {"name": "Maracaibo", "lon": -71.64, "lat": 10.64, "region": "Americas", "type": "export"},
    {"name": "Santos", "lon": -46.33, "lat": -23.95, "region": "Americas", "type": "import"},
    {"name": "Valdez", "lon": -146.35, "lat": 61.13, "region": "Americas", "type": "export"},

    # Russia/CIS
    {"name": "Novorossiysk", "lon": 37.77, "lat": 44.72, "region": "Russia", "type": "export"},
    {"name": "Primorsk", "lon": 29.52, "lat": 60.35, "region": "Russia", "type": "export"},
    {"name": "Kozmino", "lon": 133.08, "lat": 42.73, "region": "Russia", "type": "export"},

    # Additional Middle East ports
    {"name": "Jubail", "lon": 49.66, "lat": 27.01, "region": "Middle East", "type": "export"},
    {"name": "Shuaiba", "lon": 48.17, "lat": 29.03, "region": "Middle East", "type": "export"},
    {"name": "Mina Al Ahmadi", "lon": 48.17, "lat": 29.08, "region": "Middle East", "type": "export"},
    {"name": "Das Island", "lon": 52.87, "lat": 25.15, "region": "Middle East", "type": "export"},
    {"name": "Jebel Dhanna", "lon": 52.58, "lat": 24.19, "region": "Middle East", "type": "export"},
    {"name": "Sohar", "lon": 56.63, "lat": 24.36, "region": "Middle East", "type": "export"},
    {"name": "Aden", "lon": 45.03, "lat": 12.78, "region": "Middle East", "type": "hub"},
    {"name": "Hodeidah", "lon": 42.95, "lat": 14.80, "region": "Middle East", "type": "export"},
    {"name": "Bandar Abbas", "lon": 56.28, "lat": 27.19, "region": "Middle East", "type": "export"},
    {"name": "Lavan Island", "lon": 53.36, "lat": 26.81, "region": "Middle East", "type": "export"},
    {"name": "Sirri Island", "lon": 54.54, "lat": 25.91, "region": "Middle East", "type": "export"},
    {"name": "Khor Fakkan", "lon": 56.35, "lat": 25.34, "region": "Middle East", "type": "export"},

    # Additional Asia ports
    {"name": "Dalian", "lon": 121.62, "lat": 38.91, "region": "Asia", "type": "import"},
    {"name": "Tianjin", "lon": 117.70, "lat": 39.02, "region": "Asia", "type": "import"},
    {"name": "Guangzhou", "lon": 113.26, "lat": 23.13, "region": "Asia", "type": "import"},
    {"name": "Shenzhen", "lon": 114.06, "lat": 22.54, "region": "Asia", "type": "import"},
    {"name": "Zhoushan", "lon": 122.21, "lat": 29.99, "region": "Asia", "type": "import"},
    {"name": "Ulsan", "lon": 129.31, "lat": 35.54, "region": "Asia", "type": "import"},
    {"name": "Incheon", "lon": 126.70, "lat": 37.46, "region": "Asia", "type": "import"},
    {"name": "Nagoya", "lon": 136.91, "lat": 35.18, "region": "Asia", "type": "import"},
    {"name": "Osaka", "lon": 135.50, "lat": 34.69, "region": "Asia", "type": "import"},
    {"name": "Kobe", "lon": 135.19, "lat": 34.69, "region": "Asia", "type": "import"},
    {"name": "Mizushima", "lon": 133.71, "lat": 34.51, "region": "Asia", "type": "import"},
    {"name": "Sakai", "lon": 135.49, "lat": 34.57, "region": "Asia", "type": "import"},
    {"name": "Tanjung Pelepas", "lon": 103.55, "lat": 1.36, "region": "Asia", "type": "hub"},
    {"name": "Port Klang", "lon": 101.39, "lat": 2.99, "region": "Asia", "type": "hub"},
    {"name": "Penang", "lon": 100.37, "lat": 5.42, "region": "Asia", "type": "import"},
    {"name": "Laem Chabang", "lon": 100.88, "lat": 13.08, "region": "Asia", "type": "import"},
    {"name": "Map Ta Phut", "lon": 101.15, "lat": 12.71, "region": "Asia", "type": "import"},
    {"name": "Ho Chi Minh City", "lon": 106.63, "lat": 10.76, "region": "Asia", "type": "import"},
    {"name": "Hai Phong", "lon": 106.68, "lat": 20.86, "region": "Asia", "type": "import"},
    {"name": "Manila", "lon": 120.98, "lat": 14.60, "region": "Asia", "type": "import"},
    {"name": "Batangas", "lon": 121.05, "lat": 13.76, "region": "Asia", "type": "import"},
    {"name": "Surabaya", "lon": 112.75, "lat": -7.25, "region": "Asia", "type": "import"},
    {"name": "Jakarta", "lon": 106.85, "lat": -6.21, "region": "Asia", "type": "import"},
    {"name": "Balikpapan", "lon": 116.83, "lat": -1.27, "region": "Asia", "type": "export"},
    {"name": "Dumai", "lon": 101.45, "lat": 1.68, "region": "Asia", "type": "export"},
    {"name": "Mangalore", "lon": 74.84, "lat": 12.91, "region": "Asia", "type": "import"},
    {"name": "Cochin", "lon": 76.27, "lat": 9.97, "region": "Asia", "type": "import"},
    {"name": "Kandla", "lon": 70.22, "lat": 23.03, "region": "Asia", "type": "import"},
    {"name": "Paradip", "lon": 86.61, "lat": 20.26, "region": "Asia", "type": "import"},
    {"name": "Haldia", "lon": 88.06, "lat": 22.03, "region": "Asia", "type": "import"},
    {"name": "Chittagong", "lon": 91.84, "lat": 22.34, "region": "Asia", "type": "import"},
    {"name": "Colombo", "lon": 79.86, "lat": 6.93, "region": "Asia", "type": "hub"},
    {"name": "Hambantota", "lon": 81.12, "lat": 6.12, "region": "Asia", "type": "hub"},
    {"name": "Karachi", "lon": 67.01, "lat": 24.86, "region": "Asia", "type": "import"},
    {"name": "Port Qasim", "lon": 67.35, "lat": 24.78, "region": "Asia", "type": "import"},

    # Additional Europe ports
    {"name": "Gdansk", "lon": 18.65, "lat": 54.35, "region": "Europe", "type": "import"},
    {"name": "Gothenburg", "lon": 11.97, "lat": 57.71, "region": "Europe", "type": "import"},
    {"name": "Bergen", "lon": 5.32, "lat": 60.39, "region": "Europe", "type": "export"},
    {"name": "Mongstad", "lon": 5.03, "lat": 60.81, "region": "Europe", "type": "export"},
    {"name": "Stavanger", "lon": 5.73, "lat": 58.97, "region": "Europe", "type": "export"},
    {"name": "Fredericia", "lon": 9.75, "lat": 55.57, "region": "Europe", "type": "import"},
    {"name": "Wilhelmshaven", "lon": 8.13, "lat": 53.52, "region": "Europe", "type": "import"},
    {"name": "Bremerhaven", "lon": 8.58, "lat": 53.55, "region": "Europe", "type": "import"},
    {"name": "Dunkirk", "lon": 2.38, "lat": 51.03, "region": "Europe", "type": "import"},
    {"name": "Fos-sur-Mer", "lon": 4.95, "lat": 43.44, "region": "Europe", "type": "import"},
    {"name": "Barcelona", "lon": 2.17, "lat": 41.38, "region": "Europe", "type": "import"},
    {"name": "Valencia", "lon": -0.38, "lat": 39.47, "region": "Europe", "type": "import"},
    {"name": "Tarragona", "lon": 1.25, "lat": 41.12, "region": "Europe", "type": "import"},
    {"name": "Bilbao", "lon": -2.93, "lat": 43.26, "region": "Europe", "type": "import"},
    {"name": "La Coruna", "lon": -8.41, "lat": 43.37, "region": "Europe", "type": "import"},
    {"name": "Lisbon", "lon": -9.14, "lat": 38.72, "region": "Europe", "type": "import"},
    {"name": "Porto", "lon": -8.61, "lat": 41.15, "region": "Europe", "type": "import"},
    {"name": "Venice", "lon": 12.34, "lat": 45.44, "region": "Europe", "type": "import"},
    {"name": "Ravenna", "lon": 12.20, "lat": 44.42, "region": "Europe", "type": "import"},
    {"name": "Augusta", "lon": 15.22, "lat": 37.23, "region": "Europe", "type": "import"},
    {"name": "Piraeus", "lon": 23.65, "lat": 37.94, "region": "Europe", "type": "import"},
    {"name": "Thessaloniki", "lon": 22.94, "lat": 40.64, "region": "Europe", "type": "import"},
    {"name": "Constanta", "lon": 28.66, "lat": 44.18, "region": "Europe", "type": "import"},
    {"name": "Burgas", "lon": 27.47, "lat": 42.49, "region": "Europe", "type": "import"},
    {"name": "Istanbul", "lon": 28.98, "lat": 41.01, "region": "Europe", "type": "hub"},
    {"name": "Izmir", "lon": 27.14, "lat": 38.42, "region": "Europe", "type": "import"},
    {"name": "Mersin", "lon": 34.64, "lat": 36.80, "region": "Europe", "type": "import"},
    {"name": "Cork", "lon": -8.47, "lat": 51.90, "region": "Europe", "type": "import"},
    {"name": "Dublin", "lon": -6.26, "lat": 53.35, "region": "Europe", "type": "import"},
    {"name": "Southampton", "lon": -1.40, "lat": 50.90, "region": "Europe", "type": "import"},
    {"name": "Immingham", "lon": -0.22, "lat": 53.63, "region": "Europe", "type": "import"},
    {"name": "Teesport", "lon": -1.15, "lat": 54.60, "region": "Europe", "type": "import"},
    {"name": "Grangemouth", "lon": -3.72, "lat": 56.02, "region": "Europe", "type": "import"},

    # Additional Africa ports
    {"name": "Port Harcourt", "lon": 7.01, "lat": 4.78, "region": "Africa", "type": "export"},
    {"name": "Warri", "lon": 5.76, "lat": 5.52, "region": "Africa", "type": "export"},
    {"name": "Escravos", "lon": 5.19, "lat": 5.60, "region": "Africa", "type": "export"},
    {"name": "Qua Iboe", "lon": 7.93, "lat": 4.52, "region": "Africa", "type": "export"},
    {"name": "Brass", "lon": 6.24, "lat": 4.31, "region": "Africa", "type": "export"},
    {"name": "Malabo", "lon": 8.78, "lat": 3.75, "region": "Africa", "type": "export"},
    {"name": "Libreville", "lon": 9.45, "lat": 0.39, "region": "Africa", "type": "export"},
    {"name": "Port Gentil", "lon": 8.78, "lat": -0.72, "region": "Africa", "type": "export"},
    {"name": "Matadi", "lon": 13.44, "lat": -5.82, "region": "Africa", "type": "export"},
    {"name": "Cabinda", "lon": 12.19, "lat": -5.55, "region": "Africa", "type": "export"},
    {"name": "Soyo", "lon": 12.37, "lat": -6.13, "region": "Africa", "type": "export"},
    {"name": "Lobito", "lon": 13.54, "lat": -12.35, "region": "Africa", "type": "export"},
    {"name": "Walvis Bay", "lon": 14.51, "lat": -22.96, "region": "Africa", "type": "import"},
    {"name": "Cape Town", "lon": 18.42, "lat": -33.92, "region": "Africa", "type": "hub"},
    {"name": "Port Elizabeth", "lon": 25.57, "lat": -33.96, "region": "Africa", "type": "import"},
    {"name": "Richards Bay", "lon": 32.09, "lat": -28.80, "region": "Africa", "type": "export"},
    {"name": "Maputo", "lon": 32.57, "lat": -25.97, "region": "Africa", "type": "import"},
    {"name": "Beira", "lon": 34.84, "lat": -19.84, "region": "Africa", "type": "import"},
    {"name": "Dar es Salaam", "lon": 39.28, "lat": -6.82, "region": "Africa", "type": "import"},
    {"name": "Mombasa", "lon": 39.66, "lat": -4.04, "region": "Africa", "type": "import"},
    {"name": "Port Sudan", "lon": 37.22, "lat": 19.62, "region": "Africa", "type": "import"},
    {"name": "Djibouti", "lon": 43.15, "lat": 11.59, "region": "Africa", "type": "hub"},
    {"name": "Mogadishu", "lon": 45.34, "lat": 2.04, "region": "Africa", "type": "import"},
    {"name": "Dakar", "lon": -17.44, "lat": 14.69, "region": "Africa", "type": "import"},
    {"name": "Abidjan", "lon": -4.02, "lat": 5.32, "region": "Africa", "type": "import"},
    {"name": "Tema", "lon": -0.02, "lat": 5.62, "region": "Africa", "type": "import"},
    {"name": "Lome", "lon": 1.23, "lat": 6.14, "region": "Africa", "type": "import"},
    {"name": "Cotonou", "lon": 2.43, "lat": 6.37, "region": "Africa", "type": "import"},
    {"name": "Douala", "lon": 9.70, "lat": 4.05, "region": "Africa", "type": "import"},
    {"name": "Casablanca", "lon": -7.59, "lat": 33.59, "region": "Africa", "type": "import"},
    {"name": "Tangier", "lon": -5.81, "lat": 35.77, "region": "Africa", "type": "hub"},
    {"name": "Oran", "lon": -0.64, "lat": 35.70, "region": "Africa", "type": "import"},
    {"name": "Algiers", "lon": 3.06, "lat": 36.75, "region": "Africa", "type": "import"},
    {"name": "Tunis", "lon": 10.17, "lat": 36.81, "region": "Africa", "type": "import"},
    {"name": "Tripoli", "lon": 13.19, "lat": 32.89, "region": "Africa", "type": "export"},
    {"name": "Benghazi", "lon": 20.07, "lat": 32.12, "region": "Africa", "type": "export"},

    # Additional Americas ports
    {"name": "Los Angeles", "lon": -118.24, "lat": 34.05, "region": "Americas", "type": "import"},
    {"name": "Long Beach", "lon": -118.19, "lat": 33.77, "region": "Americas", "type": "import"},
    {"name": "San Francisco", "lon": -122.42, "lat": 37.77, "region": "Americas", "type": "import"},
    {"name": "Portland", "lon": -122.68, "lat": 45.52, "region": "Americas", "type": "import"},
    {"name": "Seattle", "lon": -122.33, "lat": 47.61, "region": "Americas", "type": "import"},
    {"name": "Tacoma", "lon": -122.44, "lat": 47.25, "region": "Americas", "type": "import"},
    {"name": "Anacortes", "lon": -122.61, "lat": 48.51, "region": "Americas", "type": "import"},
    {"name": "Cherry Point", "lon": -122.76, "lat": 48.86, "region": "Americas", "type": "import"},
    {"name": "Prince Rupert", "lon": -130.32, "lat": 54.31, "region": "Americas", "type": "import"},
    {"name": "Vancouver", "lon": -123.11, "lat": 49.28, "region": "Americas", "type": "import"},
    {"name": "New Orleans", "lon": -90.07, "lat": 29.95, "region": "Americas", "type": "hub"},
    {"name": "Texas City", "lon": -94.90, "lat": 29.38, "region": "Americas", "type": "export"},
    {"name": "Port Arthur", "lon": -93.93, "lat": 29.90, "region": "Americas", "type": "export"},
    {"name": "Beaumont", "lon": -94.10, "lat": 30.08, "region": "Americas", "type": "export"},
    {"name": "Lake Charles", "lon": -93.22, "lat": 30.23, "region": "Americas", "type": "export"},
    {"name": "Baton Rouge", "lon": -91.15, "lat": 30.45, "region": "Americas", "type": "export"},
    {"name": "Mobile", "lon": -88.04, "lat": 30.69, "region": "Americas", "type": "import"},
    {"name": "Tampa", "lon": -82.46, "lat": 27.95, "region": "Americas", "type": "import"},
    {"name": "Jacksonville", "lon": -81.66, "lat": 30.33, "region": "Americas", "type": "import"},
    {"name": "Savannah", "lon": -81.10, "lat": 32.08, "region": "Americas", "type": "import"},
    {"name": "Charleston", "lon": -79.93, "lat": 32.78, "region": "Americas", "type": "import"},
    {"name": "Baltimore", "lon": -76.61, "lat": 39.29, "region": "Americas", "type": "import"},
    {"name": "Boston", "lon": -71.06, "lat": 42.36, "region": "Americas", "type": "import"},
    {"name": "Halifax", "lon": -63.57, "lat": 44.65, "region": "Americas", "type": "import"},
    {"name": "Saint John", "lon": -66.06, "lat": 45.27, "region": "Americas", "type": "import"},
    {"name": "Montreal", "lon": -73.57, "lat": 45.50, "region": "Americas", "type": "import"},
    {"name": "Toronto", "lon": -79.38, "lat": 43.65, "region": "Americas", "type": "import"},
    {"name": "Panama City", "lon": -79.52, "lat": 8.98, "region": "Americas", "type": "hub"},
    {"name": "Colon", "lon": -79.90, "lat": 9.36, "region": "Americas", "type": "hub"},
    {"name": "Puerto Limon", "lon": -83.03, "lat": 10.00, "region": "Americas", "type": "import"},
    {"name": "Veracruz", "lon": -96.13, "lat": 19.20, "region": "Americas", "type": "import"},
    {"name": "Tampico", "lon": -97.85, "lat": 22.25, "region": "Americas", "type": "export"},
    {"name": "Altamira", "lon": -97.93, "lat": 22.40, "region": "Americas", "type": "import"},
    {"name": "Tuxpan", "lon": -97.40, "lat": 20.96, "region": "Americas", "type": "export"},
    {"name": "Lazaro Cardenas", "lon": -102.20, "lat": 17.96, "region": "Americas", "type": "import"},
    {"name": "Manzanillo", "lon": -104.32, "lat": 19.05, "region": "Americas", "type": "import"},
    {"name": "Havana", "lon": -82.36, "lat": 23.14, "region": "Americas", "type": "import"},
    {"name": "Kingston", "lon": -76.79, "lat": 17.97, "region": "Americas", "type": "hub"},
    {"name": "San Juan", "lon": -66.11, "lat": 18.47, "region": "Americas", "type": "import"},
    {"name": "Point Lisas", "lon": -61.47, "lat": 10.41, "region": "Americas", "type": "export"},
    {"name": "Point Fortin", "lon": -61.68, "lat": 10.18, "region": "Americas", "type": "export"},
    {"name": "Curacao", "lon": -68.99, "lat": 12.17, "region": "Americas", "type": "hub"},
    {"name": "Aruba", "lon": -70.03, "lat": 12.52, "region": "Americas", "type": "hub"},
    {"name": "Puerto La Cruz", "lon": -64.64, "lat": 10.21, "region": "Americas", "type": "export"},
    {"name": "Jose", "lon": -64.93, "lat": 10.48, "region": "Americas", "type": "export"},
    {"name": "Amuay Bay", "lon": -70.22, "lat": 11.77, "region": "Americas", "type": "export"},
    {"name": "Barranquilla", "lon": -74.80, "lat": 10.96, "region": "Americas", "type": "import"},
    {"name": "Buenaventura", "lon": -77.04, "lat": 3.88, "region": "Americas", "type": "import"},
    {"name": "Guayaquil", "lon": -79.88, "lat": -2.19, "region": "Americas", "type": "import"},
    {"name": "Callao", "lon": -77.15, "lat": -12.07, "region": "Americas", "type": "import"},
    {"name": "Antofagasta", "lon": -70.40, "lat": -23.65, "region": "Americas", "type": "import"},
    {"name": "Valparaiso", "lon": -71.63, "lat": -33.05, "region": "Americas", "type": "import"},
    {"name": "San Antonio", "lon": -71.62, "lat": -33.59, "region": "Americas", "type": "import"},
    {"name": "Buenos Aires", "lon": -58.38, "lat": -34.60, "region": "Americas", "type": "import"},
    {"name": "La Plata", "lon": -57.95, "lat": -34.92, "region": "Americas", "type": "import"},
    {"name": "Montevideo", "lon": -56.16, "lat": -34.90, "region": "Americas", "type": "import"},
    {"name": "Rio de Janeiro", "lon": -43.17, "lat": -22.91, "region": "Americas", "type": "import"},
    {"name": "Paranagua", "lon": -48.51, "lat": -25.52, "region": "Americas", "type": "import"},
    {"name": "Rio Grande", "lon": -52.10, "lat": -32.03, "region": "Americas", "type": "import"},

    # Additional Russia/CIS ports
    {"name": "Murmansk", "lon": 33.09, "lat": 68.97, "region": "Russia", "type": "export"},
    {"name": "Arkhangelsk", "lon": 40.54, "lat": 64.54, "region": "Russia", "type": "export"},
    {"name": "St Petersburg", "lon": 30.31, "lat": 59.93, "region": "Russia", "type": "export"},
    {"name": "Ust-Luga", "lon": 28.40, "lat": 59.68, "region": "Russia", "type": "export"},
    {"name": "Vysotsk", "lon": 28.57, "lat": 60.63, "region": "Russia", "type": "export"},
    {"name": "Tuapse", "lon": 39.08, "lat": 44.10, "region": "Russia", "type": "export"},
    {"name": "Taman", "lon": 36.72, "lat": 45.21, "region": "Russia", "type": "export"},
    {"name": "Nakhodka", "lon": 132.88, "lat": 42.82, "region": "Russia", "type": "export"},
    {"name": "De-Kastri", "lon": 140.79, "lat": 51.47, "region": "Russia", "type": "export"},
    {"name": "Sakhalin", "lon": 142.73, "lat": 46.96, "region": "Russia", "type": "export"},
    {"name": "Aktau", "lon": 51.15, "lat": 43.65, "region": "Russia", "type": "export"},
    {"name": "Baku", "lon": 49.87, "lat": 40.41, "region": "Russia", "type": "export"},
    {"name": "Batumi", "lon": 41.64, "lat": 41.64, "region": "Russia", "type": "export"},
    {"name": "Poti", "lon": 41.67, "lat": 42.15, "region": "Russia", "type": "export"},
    {"name": "Supsa", "lon": 41.82, "lat": 42.01, "region": "Russia", "type": "export"},
    {"name": "Ceyhan", "lon": 35.82, "lat": 36.68, "region": "Russia", "type": "export"},
])

n_ports = len(ports)
print(f"Created {n_ports} oil ports across {ports['region'].nunique()} regions")

# %%

# =============================================================================
# Generate shipping routes (10,000 edges with weights)
# =============================================================================

# Vessel weight classes (deadweight tonnage in thousands)
vessel_classes = {
    "VLCC": {"min_dwt": 200, "max_dwt": 320, "probability": 0.15},      # Very Large Crude Carrier
    "Suezmax": {"min_dwt": 120, "max_dwt": 200, "probability": 0.25},   # Max size for Suez Canal
    "Aframax": {"min_dwt": 80, "max_dwt": 120, "probability": 0.30},    # Average Freight Rate Assessment
    "Panamax": {"min_dwt": 60, "max_dwt": 80, "probability": 0.20},     # Max size for Panama Canal
    "Handysize": {"min_dwt": 15, "max_dwt": 60, "probability": 0.10},   # Smaller tankers
}

def get_route_probability(source_type, target_type, source_region, target_region):
    """Calculate probability weight for a route based on realistic trade patterns."""
    prob = 1.0

    # Export to import routes are most common
    if source_type == "export" and target_type == "import":
        prob *= 3.0
    elif source_type == "export" and target_type == "hub":
        prob *= 2.5
    elif source_type == "hub" and target_type == "import":
        prob *= 2.0
    elif source_type == "hub" and target_type == "hub":
        prob *= 1.5

    # Major trade flows
    if source_region == "Middle East" and target_region == "Asia":
        prob *= 4.0  # Largest oil trade route in the world
    elif source_region == "Middle East" and target_region == "Europe":
        prob *= 2.5
    elif source_region == "Africa" and target_region == "Europe":
        prob *= 2.0
    elif source_region == "Africa" and target_region == "Asia":
        prob *= 1.8
    elif source_region == "Russia" and target_region == "Europe":
        prob *= 2.0
    elif source_region == "Russia" and target_region == "Asia":
        prob *= 2.5
    elif source_region == "Americas" and target_region == "Europe":
        prob *= 1.5
    elif source_region == "Americas" and target_region == "Asia":
        prob *= 1.8

    return prob

# Build probability matrix for route selection
route_probs = np.zeros((n_ports, n_ports))
for i in range(n_ports):
    for j in range(n_ports):
        if i != j:
            route_probs[i, j] = get_route_probability(
                ports.iloc[i]['type'], ports.iloc[j]['type'],
                ports.iloc[i]['region'], ports.iloc[j]['region']
            )

# Normalize probabilities
route_probs_flat = route_probs.flatten()
route_probs_flat = route_probs_flat / route_probs_flat.sum()

# Generate 10,000 shipping movements
edge_indices = np.random.choice(
    n_ports * n_ports,
    size=n_edges,
    replace=True,
    p=route_probs_flat
)

# Convert flat indices back to (source, target) pairs
sources = edge_indices // n_ports
targets = edge_indices % n_ports

# Assign vessel classes based on route characteristics
def assign_vessel_class(source_idx, target_idx):
    """Assign vessel class based on route - longer routes tend to use larger vessels."""
    source = ports.iloc[source_idx]
    target = ports.iloc[target_idx]

    # Calculate approximate distance (simple Euclidean for weighting)
    dist = np.sqrt((source['lon'] - target['lon'])**2 + (source['lat'] - target['lat'])**2)

    # Long-haul routes favor VLCCs
    if dist > 100:  # ~intercontinental
        class_probs = {"VLCC": 0.4, "Suezmax": 0.35, "Aframax": 0.15, "Panamax": 0.07, "Handysize": 0.03}
    elif dist > 50:  # ~regional
        class_probs = {"VLCC": 0.2, "Suezmax": 0.35, "Aframax": 0.30, "Panamax": 0.10, "Handysize": 0.05}
    else:  # Short haul
        class_probs = {"VLCC": 0.05, "Suezmax": 0.15, "Aframax": 0.35, "Panamax": 0.30, "Handysize": 0.15}

    classes = list(class_probs.keys())
    probs = list(class_probs.values())
    return np.random.choice(classes, p=probs)

# Generate vessel weights (cargo capacity in thousands of DWT)
vessel_weights = []
vessel_types = []
for s, t in zip(sources, targets):
    v_class = assign_vessel_class(s, t)
    vessel_types.append(v_class)
    v_info = vessel_classes[v_class]
    weight = np.random.uniform(v_info['min_dwt'], v_info['max_dwt'])
    vessel_weights.append(weight)

vessel_weights = np.array(vessel_weights)

# Create edges DataFrame
edges_df = pd.DataFrame({
    'source': sources,
    'target': targets,
    'x': ports.iloc[sources]['lon'].values,
    'y': ports.iloc[sources]['lat'].values,
    'xend': ports.iloc[targets]['lon'].values,
    'yend': ports.iloc[targets]['lat'].values,
    'weight': vessel_weights,
    'vessel_class': vessel_types
})

print(f"\nGenerated {len(edges_df)} shipping movements")
print(f"\nVessel class distribution:")
print(edges_df['vessel_class'].value_counts())
print(f"\nWeight statistics (thousand DWT):")
print(edges_df['weight'].describe())

# %%
# =============================================================================
# Create igraph object for visualization
# =============================================================================

g = ig.Graph(directed=True)
g.add_vertices(n_ports)

# Set vertex attributes
g.vs['name'] = ports['name'].tolist()
g.vs['longitude'] = ports['lon'].tolist()
g.vs['latitude'] = ports['lat'].tolist()
g.vs['region'] = ports['region'].tolist()
g.vs['type'] = ports['type'].tolist()

# Add edges with weights
g.add_edges(list(zip(sources, targets)))
g.es['weight'] = vessel_weights.tolist()
g.es['vessel_class'] = vessel_types

print(f"\nCreated igraph with {g.vcount()} vertices and {g.ecount()} edges")

# %%
# =============================================================================
# Visualize with edge bundling
# =============================================================================

print("\n" + "="*60)
print("Creating visualization with weighted edge bundling...")
print("Heavier shipping routes (VLCCs) will attract lighter routes")
print("="*60 + "\n")

# Create the edgebundle geom first (extracts data from igraph)
bundle = geom_edgebundle(
    graph=g,
    # weight is auto-detected from graph's edge 'weight' attribute
    compatibility_threshold=0.6,
    C=6,
    I=50,
    E=1.0,
    color='#ff6b35',
    alpha=0.4,
    linewidth=0.3,
    show_highlight=True,
    highlight_color='#ffd700',
    highlight_alpha=0.15,
    highlight_width=0.1,
    show_nodes=True,
    node_color='#00ff88',
    node_size=4,
    node_alpha=0.9,
    verbose=True
)

# Create the visualization using extracted data
fig = (
    ggplot(bundle.data, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_map(
        map_type='world',
        landcolor='#1a1a2e',
        oceancolor='#0f0f1a',
        countrycolor='#2d2d44',
        coastlinecolor='#3d3d5c',
        bgcolor='#0a0a14'
    )
    + bundle
    + theme_dark()
    + labs(
        title='Global Oil Tanker Shipping Network',
        subtitle='10,000 simulated vessel movements with weighted edge bundling (heavier vessels = stronger bundling attraction)'
    )
)

# Draw and show
figure = fig.draw()

# Update layout for better presentation
figure.update_layout(
    geo=dict(
        projection_type='natural earth',
        showland=True,
        showocean=True,
        showcoastlines=True,
        showcountries=True,
        landcolor='#1a1a2e',
        oceancolor='#0f0f1a',
        countrycolor='#2d2d44',
        coastlinecolor='#3d3d5c',
        bgcolor='#0a0a14',
        lonaxis=dict(range=[-180, 180]),
        lataxis=dict(range=[-60, 75]),
    ),
    paper_bgcolor='#0a0a14',
    title=dict(
        text='<b>Global Oil Tanker Shipping Network</b><br><sup>10,000 simulated movements | Weighted edge bundling (VLCC routes attract lighter traffic)</sup>',
        font=dict(color='white', size=16),
        x=0.5,
        xanchor='center'
    ),
    margin=dict(l=0, r=0, t=60, b=0),
)

figure.show()

# %%

# =============================================================================
# Summary statistics
# =============================================================================

print("\n" + "="*60)
print("SHIPPING NETWORK SUMMARY")
print("="*60)

print(f"\nTop 10 busiest routes:")
route_counts = edges_df.groupby(['source', 'target']).agg({
    'weight': ['count', 'sum', 'mean']
}).reset_index()
route_counts.columns = ['source', 'target', 'n_shipments', 'total_dwt', 'avg_dwt']
route_counts['source_name'] = route_counts['source'].map(lambda x: ports.iloc[x]['name'])
route_counts['target_name'] = route_counts['target'].map(lambda x: ports.iloc[x]['name'])
route_counts = route_counts.sort_values('total_dwt', ascending=False)

for _, row in route_counts.head(10).iterrows():
    print(f"  {row['source_name']:20} → {row['target_name']:20}: "
          f"{int(row['n_shipments']):4} ships, {row['total_dwt']/1000:.1f}M DWT total")

print(f"\nRegional trade flows (million DWT):")
edges_df['source_region'] = edges_df['source'].map(lambda x: ports.iloc[x]['region'])
edges_df['target_region'] = edges_df['target'].map(lambda x: ports.iloc[x]['region'])
regional_flows = edges_df.groupby(['source_region', 'target_region'])['weight'].sum() / 1000
regional_flows = regional_flows.sort_values(ascending=False)
for (src, tgt), flow in regional_flows.head(10).items():
    print(f"  {src:15} → {tgt:15}: {flow:.1f}M DWT")

# %%