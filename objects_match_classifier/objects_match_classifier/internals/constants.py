
# Hotel constants

# tourism=hotel or building=hotel or tourism=chalet or
# building=bungalow or tourism=guest_house or tourism=apartment or 
# tourism=hostel or tourism=motel or tourism=alpine_hut or 
# tourism=wilderness_hut or tourism=camp_site or tourism=caravan_site or 
# tourism=camp_pitch or amenity=love_hotel or building=dormitory or 
# leisure=resort or leisure=beach_resort
TOURISM_HOTELS = {
    'hotel', 'chalet', 'guest_house', 
    'apartment', 'hostel', 'motel', 
    'alpine_hut', 'wilderness_hut', 'camp_site',
    'caravan_site', 'camp_pitch'
}
BUILDING_HOTELS = {'hotel', 'bungalow', 'dormitory'}
AMENITY_HOTELS = {'love_hotel', }
LEISURE_HOTELS = {'resort', 'beach_resort', }

B_COLS = ['other_id', 'other_name', 'other_lat', 'other_lon']
