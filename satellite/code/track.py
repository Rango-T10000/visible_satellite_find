import os
from datetime import datetime, timezone
from skyfield.api import Topos, load, EarthSatellite
import urllib.request


def download_tle(tle_file, tle_url):

    urllib.request.urlretrieve(tle_url, tle_file)
    
    """Download TLE data if the file doesn't exist or is more than 1 day old."""
    file_exists = os.path.exists(tle_file)
    file_is_old = (datetime.now(timezone.utc) - datetime.fromtimestamp(os.path.getmtime(tle_file), timezone.utc)).total_seconds() > 86400
    
    if not file_exists or file_is_old:
        load.tle_file(tle_url, filename=tle_file, reload=True)
    else:
        load.tle_file(tle_url, filename=tle_file, reload=False)


def find_visible_starlink(latitude, longitude):
    # TLE file settings
    tle_file = 'satellite/code/starlink.txt'
    tle_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle'
    #在这个链接找到starlink
    #https://celestrak.org/NORAD/elements/

    # Download TLE data if necessary
    download_tle(tle_file, tle_url)

    # Load TLE data
    ts = load.timescale()
    t = ts.utc(datetime.now(timezone.utc))
    satellites = load.tle_file(tle_file)

    # Set up observer's location
    observer = Topos(latitude_degrees=latitude, longitude_degrees=longitude)

    # Check for visible Starlink satellites
    for satellite in satellites:
        difference = satellite - observer
        topocentric = difference.at(t)
        alt, az, distance = topocentric.altaz()

        if alt.degrees > 0:  # Satellite is above the horizon
            return satellite.name

    return None


def main():
    # Replace with your latitude and longitude
    my_latitude = 40.7128  # Example latitude (New York City)
    my_longitude = -74.0060  # Example longitude (New York City)

    visible_satellite_name = find_visible_starlink(my_latitude, my_longitude)
    if visible_satellite_name:
        print(f"Visible Starlink Satellite: {visible_satellite_name}")
    else:
        print("No Starlink satellites are currently visible from your location.")

if __name__ == '__main__':
    main()
