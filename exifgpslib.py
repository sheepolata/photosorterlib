from exif import Image
from geopy.geocoders import Nominatim


def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == 'S' or ref == 'W':
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def get_location_data(image_path):
    try:
        with open(image_path, 'rb') as src:
            img = Image(src)

        lat = decimal_coords(img.gps_latitude, img.gps_latitude_ref)
        lon = decimal_coords(img.gps_longitude, img.gps_longitude_ref)

        address = Nominatim(user_agent='GetLoc')
        location = address.reverse(f'{lat}, {lon}')

        _loc_list = str(location).split(',')
        location_dict = {
            "Country":_loc_list[-1],
            "Postcode": _loc_list[-2],
            "Region": _loc_list[-4],
            "Dept": _loc_list[-5],
            "City": _loc_list[-6],
        }

        return location_dict
    except AttributeError:
        return {"nodata":True}
