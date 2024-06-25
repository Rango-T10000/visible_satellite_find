from track import download_tle
from skyfield.api import Topos, load, EarthSatellite
from datetime import datetime, timezone, timedelta
import csv


def get_visible_satellites(latitude, longitude, start_time, end_time, interval_minutes=1):
    tle_file = 'satellite/code/starlink.txt'
    tle_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle'
    download_tle(tle_file, tle_url)

    ts = load.timescale()
    observer = Topos(latitude_degrees=latitude, longitude_degrees=longitude)

    satellites = load.tle_file(tle_file)
    visible_passes = []

    current_time = start_time
    while current_time <= end_time:
        t = ts.from_datetime(current_time)
        for satellite in satellites:
            difference = satellite - observer
            topocentric = difference.at(t)
            alt, az, distance = topocentric.altaz()
            if alt.degrees > 40:  # Satellite is above the horizon
                visible_passes.append((satellite.name, current_time))
                break  # Move to next time slot after finding the first visible satellite
        current_time += timedelta(minutes=interval_minutes)

    return visible_passes

# Replace with your latitude and longitude
my_latitude = 33.8688  # Example latitude (Syndey)
my_longitude = -179.2093  # Example longitude (Syndey)
# my_latitude = 40.7128  # Example latitude (New York City)
# my_longitude = -74.0060  # Example longitude (New York City)


# Define the time range for a day
start_time = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
end_time = start_time + timedelta(days=1)
print(start_time, end_time)

visible_satellites = get_visible_satellites(my_latitude, my_longitude, start_time, end_time)

for name, time in visible_satellites:
    print(f"{name} visible at {time.strftime('%Y-%m-%d %H:%M:%S')} UTC")


# CSV file path
csv_file_path = 'satellite/visible_satellites.csv'

# Write the data to a CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Satellite Name', 'Visibility Time (UTC)'])

    for name, time in visible_satellites:
        writer.writerow([name, time.strftime('%Y-%m-%d %H:%M:%S')])

print(f"Data saved to {csv_file_path}")
