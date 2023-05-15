import exifread
from geopy.geocoders import Nominatim

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
    geolocator = Nominatim(user_agent="my_app")  # 사용자 에이전트 이름 설정
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    if location is None:
        return "지역을 찾을 수 없습니다."
    else:
        return location.address



# 이미지 파일 경로
image_path = '/.../HD.jpg'

image_name = image_path.split("/")[-1]
image_name = image_name.split(".")[0]


# 경도, 위도 값 출력
coordinates = get_gps_coordinates(image_path)
latitude, longitude = coordinates

latitude = f'{latitude:.6f}'
longitude = f'{longitude:.6f}'      

print(f"latitude: {latitude}")
print(f"longitude: {longitude}")

#위치 출력
location_name = get_location_name(latitude, longitude)
print(f"location: {location_name}") 

txt_name = image_name + ".txt"

#txt 파일로 저장
File =  open(f"location_save/{txt_name}", "w")
print(f"{image_path}: {location_name}", file=File)
File.close
