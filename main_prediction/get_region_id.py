from main_prediction.regions_name_map import region_map


def get_region_id(location_name):
    for region_id, region_name in region_map.items():
        if region_name.lower() == location_name.lower():
            return region_id
    return None

def get_region_name(region_id):
    return region_map.get(region_id, None)