import pandas
import folium
import re

wiglefile = pandas.read_csv('total_war.csv', delimiter=',', encoding='latin-1', header=1)



warmap = folium.Map(location=[wiglefile.CurrentLatitude.mean(), wiglefile.CurrentLongitude.mean()], zoom_start=8.3)



valid = []
seen_ssid = set()
for rows in wiglefile[['MAC', 'SSID', 'AuthMode', 'FirstSeen', 'Channel', 'RSSI', 'CurrentLatitude', 'CurrentLongitude', 'AltitudeMeters', 'AccuracyMeters', 'Type']].values:
    ssid = str(rows[1]).strip()

    
    if (
        not ssid
        or ssid in seen_ssid
        or re.search(r'[\\/<>\"\']', ssid)  # exclude slashes, quotes, angle brackets
        or not all(32 <= ord(c) <= 126 for c in ssid)  # printable ASCII only
    ):
        continue

    valid.append(rows)
    seen_ssid.add(ssid)


valid_devices = pandas.DataFrame(valid).dropna()
valid_devices.columns = ['MAC', 'SSID', 'AuthMode', 'FirstSeen', 'Channel', 'RSSI', 'CurrentLatitude', 'CurrentLongitude', 'AltitudeMeters', 'AccuracyMeters', 'Type']





for device in valid_devices[['SSID', 'MAC', 'AuthMode', 'CurrentLatitude', 'CurrentLongitude', 'AltitudeMeters']].values:
    pop = f"SSID: {device[0]} MAC: {device[1]} Security: {device[2]} Altitude: {device[5]}"
    folium.CircleMarker(location=[device[3], device[4]], radius=5, max_width=500, color='purple', popup=folium.Popup(html=pop, parse_html=True)).add_to(warmap)

warmap.save('total_war.html')








