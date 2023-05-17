import exifread
from geopy.geocoders import Nominatim
import argparse
import cv2

def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1]
    seconds = dms[2]
    decimal_value = degrees + minutes / 60.0 + seconds / 3600.0
    if ref in ['S', 'W']:
        decimal_value = -decimal_value
    return decimal_value

def get_gps_coordinates(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f, details=False)

    if 'GPS GPSLongitude' in tags and 'GPS GPSLatitude' in tags:
        longitude_dms = tags['GPS GPSLongitude'].values
        longitude_ref = tags['GPS GPSLongitudeRef'].values
        latitude_dms = tags['GPS GPSLatitude'].values
        latitude_ref = tags['GPS GPSLatitudeRef'].values

        longitude = get_decimal_from_dms(longitude_dms, longitude_ref)
        latitude = get_decimal_from_dms(latitude_dms, latitude_ref)

        return latitude, longitude
    else:
        return None

def get_location_name(latitude, longitude):
    geolocator = Nominatim(user_agent="my_app")  # Set your own user agent name
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    if location is None:
        return "지역을 찾을 수 없습니다."
    else:
        return location.address

# Create an argument parser
parser = argparse.ArgumentParser(description='Retrieve GPS coordinates and location information from an image.')

# Add an argument for the image path
parser.add_argument('image_path', type=str, help='path to the image file')

# Parse the arguments
args = parser.parse_args()

# Get the image path from the arguments
image_path = args.image_path

image_name = image_path.split("/")[-1]
image_name = image_name.split(".")[0]

# Get the GPS coordinates
coordinates = get_gps_coordinates(image_path)
if coordinates is None:
    print("No GPS coordinates found in the image.")
    exit()

latitude, longitude = coordinates

latitude = f'{latitude:.6f}'
longitude = f'{longitude:.6f}'      

print(f"latitude: {latitude}")
print(f"longitude: {longitude}")

# Get the location name
location_name = get_location_name(latitude, longitude)
print(f"location: {location_name}") 

txt_name = image_name + ".txt"

save_img = cv2.imread(image_path)
cv2.imwrite(f"location_save/{image_name}.jpg", save_img)

# Save the location to a text file
file = open(f"location_save/{txt_name}", "w")
print(f"{image_path}: {location_name}", file=file)
file.close()
