import oceans2 as o2


def test_search_location():
    filters = {'locationName': 'Burrard'}
    results = o2.get_location_codes(filters)
    assert results[0]["locationCode"] == "BIIP"


def test_search_product():
    filters = {'locationCode': 'BISS',
               'deviceCode': 'TDKLAMBDA15C3256AB'}
    results = o2.get_data_product_codes(filters)
    assert results[0]["dataProductCode"] == 'LF'


def test_search_device():
    filters = {'locationCode': 'BISS'}
    results = o2.get_device_codes(filters)
    assert results[1]["deviceCode"] == 'TDKLAMBDA15C3256AB'


def test_search_category():
    filters = {'deviceCategoryCode': 'CTD'}
    results = o2.get_location_code_by_category(filters)
    assert results[0]["locationCode"] == 'AS04'
