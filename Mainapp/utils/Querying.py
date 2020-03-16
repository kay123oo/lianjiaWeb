from .find_conditions import *
from mongoengine.queryset.visitor import Q


class GetQuerying():
    def getQ_by_rp(self, prices):
        resQ = Q()
        for price in prices:
            if int(price) == PriceConditions.PRICE_00.value:
                resQ = resQ | Q(price__lte=1000)
            elif int(price) == PriceConditions.PRICE_01.value:
                resQ = resQ | (Q(price__gt=1000) & Q(price__lte=1500))
            elif int(price) == PriceConditions.PRICE_02.value:
                resQ = resQ | (Q(price__gt=1500) & Q(price__lte=2000))
            elif int(price) == PriceConditions.PRICE_03.value:
                resQ = resQ | (Q(price__gt=2000) & Q(price__lte=2500))
            elif int(price) == PriceConditions.PRICE_04.value:
                resQ = resQ | (Q(price__gt=2500) & Q(price__lte=3000))
            elif int(price) == PriceConditions.PRICE_05.value:
                resQ = resQ | (Q(price__gt=3000) & Q(price__lte=5000))
            elif int(price) == PriceConditions.PRICE_06.value:
                resQ = resQ | (Q(price__gte=5000))
        return resQ


    def getQ_by_house_tyoe(self, houseTypes):
        resQ = Q()
        for ht in houseTypes:
            ht = int(ht)
            if ht == HouseTypeConditions.One_LivingRoom.value:
                resQ = resQ | Q(hall_num=1)
            elif ht == HouseTypeConditions.Tow_LivingRooms.value:
                resQ = resQ | Q(hall_num=2)
            elif ht == HouseTypeConditions.Three_LivingRooms.value:
                resQ = resQ | Q(hall_num=3)
            elif ht == HouseTypeConditions.More_Than_Four_LivingRooms.value:
                resQ = resQ | Q(hall_num__gte=4)
        return resQ

    def getQ_by_orientation(self, orientations):
        resQ = Q()
        for o in orientations:
            o = int(o)
            if o == OrientationConditions.Eastward.value:
                resQ = resQ | Q(orientation='东')
            elif o == OrientationConditions.Southward.value:
                resQ = resQ | Q(orientation='南')
            elif o == OrientationConditions.Westward.value:
                resQ = resQ | Q(orientation='西')
            elif o == OrientationConditions.Northward.value:
                resQ = resQ | Q(orientation='北')
            elif o == OrientationConditions.Southwestward.value:
                resQ = resQ | Q(orientation='西南')
        return resQ

    def getQ_by_floor(self, floor):
        resQ = Q()
        for f in floor:
            f = int(f)
            if f == FloorConditions.FLOOR_LOW.value:
                resQ = resQ | Q(floor__lte=3)
            elif f == FloorConditions.FLOOR_MID.value:
                resQ = resQ | (Q(floor__gt=3) & Q(floor__lte=6))
            elif f == FloorConditions.FLOOR_HIGH.value:
                resQ = resQ | Q(floor__gt=6)
        return resQ

    def getQ_by_tags(self, tags):
        resQ = Q()
        for tag in tags:
            tag = int(tag)
            if tag == FeaturesTag.Near_Subway.value:
                resQ = resQ & Q(tags='近地铁')
            elif tag == FeaturesTag.Decorated.value:
                resQ = resQ & Q(tags='精装')
            elif tag == FeaturesTag.Central_Heating.value:
                resQ = resQ & Q(tags='集中供暖')
            elif tag == FeaturesTag.Visit_House_Anytime.value:
                resQ = resQ & Q(tags='随时看房')
            elif tag == FeaturesTag.Double_Toilet.value:
                resQ = resQ & Q(tags='双卫生间')
        return resQ

    def getQ_by_rentType(self, rentTpye):
        resQ = Q()
        rentTpye = int(rentTpye)
        if rentTpye == RentTypeConditions.Joint_Rent.value:
            resQ = Q(title__contains='合租')
        elif rentTpye == RentTypeConditions.Entire_Rent.value:
            resQ = Q(title__contains='整租')
        elif rentTpye == RentTypeConditions.Apartment.value:
            resQ = Q(dataDistributionType=0)
        return resQ


GetQuerying=GetQuerying()