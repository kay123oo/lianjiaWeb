from enum import IntEnum


class PriceConditions(IntEnum):
    PRICE_00 = 0
    PRICE_01 = 1
    PRICE_02 = 2
    PRICE_03 = 3
    PRICE_04 = 4
    PRICE_05 = 5
    PRICE_06 = 6
    PRICE_07 = 7


class RentTypeConditions(IntEnum):
    Joint_Rent = 0
    Entire_Rent = 1
    Apartment = 2


class OrientationConditions(IntEnum):
    Eastward = 0
    Westward = 1
    Southward = 2
    Northward = 3
    Southwestward = 4


class HouseTypeConditions(IntEnum):
    One_LivingRoom = 0
    Tow_LivingRooms = 1
    Three_LivingRooms = 2
    More_Than_Four_LivingRooms = 3


class FloorConditions(IntEnum):
    FLOOR_LOW = 0
    FLOOR_MID = 1
    FLOOR_HIGH = 2


class ElevatorConditions(IntEnum):
    ELEVATOR = 0
    NO_ELEVATOR = 1


class SortingWays(IntEnum):
    Sort_By_Price = 0
    Sort_By_Area = 1


class FeaturesTag(IntEnum):
    Near_Subway = 0
    Decorated = 1
    Central_Heating = 2
    Double_Toilet = 3
    Visit_House_Anytime = 4






