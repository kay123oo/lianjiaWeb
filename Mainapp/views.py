from django.shortcuts import render
from django.views import generic
from .models import zufang
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page
from .utils.district_and_microdistrict import DM ,ZH_EN, Cities,District_border, City_Center_Point
from mongoengine.queryset.visitor import Q
from .utils.Querying import GetQuerying
import re
from .utils.find_conditions import SortingWays
import logging
from .data_analysis.RentAnalysis import RentAnalysis


class IndexView(generic.ListView):
    template_name = "Mainapp/index2.html"
    context_object_name = "houses"

    def get_queryset(self):
        return zufang.objects.all()[:10]


@cache_page(60 * 100)
def index(request):
    data = {
        'district_house_count_pie_gz': RentAnalysis.district_house_count('广州').render_embed(),
        'district_rent_price_gz': RentAnalysis.district_rent_price('广州').render_embed(),
        'house_type_count_gz': RentAnalysis.house_type_count('广州').render_embed(),
        'orientation_count_gz': RentAnalysis.orientation_count('广州').render_embed(),
        'rent_area_count_gz': RentAnalysis.rent_area_count('广州').render_embed(),
        'microdistrict_price_top10_gz': RentAnalysis.microdistrict_price_top10('广州').render_embed(),
        'tags_count_bar_gz': RentAnalysis.tags_count_bar('广州').render_embed(),
        'rent_type_pie_gz': RentAnalysis.rent_type_pie('广州').render_embed(),

        'district_house_count_pie_sz': RentAnalysis.district_house_count('深圳').render_embed(),
        'district_rent_price_sz': RentAnalysis.district_rent_price('深圳').render_embed(),
        'house_type_count_sz': RentAnalysis.house_type_count('深圳').render_embed(),
        'orientation_count_sz': RentAnalysis.orientation_count('深圳').render_embed(),
        'rent_area_count_sz': RentAnalysis.rent_area_count('深圳').render_embed(),
        'microdistrict_price_top10_sz': RentAnalysis.microdistrict_price_top10('深圳').render_embed(),
        'tags_count_bar_sz': RentAnalysis.tags_count_bar('深圳').render_embed(),
        'rent_type_pie_sz': RentAnalysis.rent_type_pie('深圳').render_embed(),

        'district_house_count_pie_sh': RentAnalysis.district_house_count('上海').render_embed(),
        'district_rent_price_sh': RentAnalysis.district_rent_price('上海').render_embed(),
        'house_type_count_sh': RentAnalysis.house_type_count('上海').render_embed(),
        'orientation_count_sh': RentAnalysis.orientation_count('上海').render_embed(),
        'rent_area_count_sh': RentAnalysis.rent_area_count('上海').render_embed(),
        'microdistrict_price_top10_sh': RentAnalysis.microdistrict_price_top10('上海').render_embed(),
        'tags_count_bar_sh': RentAnalysis.tags_count_bar('上海').render_embed(),
        'rent_type_pie_sh': RentAnalysis.rent_type_pie('上海').render_embed(),
    }
    return render(request, 'Mainapp/base.html', data)


@cache_page(60 * 10)
def group_by_city(request, city):
    logging.info('按城市请求租房信息')
    page = request.GET.get('page')
    data = get_return_data(city=city, page=page)
    return render(request, 'Mainapp/index2.html', data)


@cache_page(60 * 10)
def group_by_district(request, city, district):
    logging.info('按区县请求租房信息')
    page = request.GET.get('page')
    data = get_return_data(city=city, district=district, page=page)
    return render(request, 'Mainapp/index2.html', data)


@cache_page(60 * 10)
def group_by_microdistrict(request, city, district, microdistrict):
    logging.info('按商圈请求租房信息')
    page = request.GET.get('page')
    data = get_return_data(city=city,
                           district=district,
                           microdistrict=microdistrict,
                           page=page)
    return render(request, 'Mainapp/index2.html', data)


@cache_page(60 * 10)
def get_by_conditions(request,  conditions, city, district="", microdistrict=""):
    logging.info('按筛选条件请求租房信息')
    resQ = Q()
    # 出租方式筛选
    rent_type = re.findall(r'rt([0-9])', conditions)
    if rent_type:
        rent_type = rent_type[0]
        resQ = resQ & GetQuerying.getQ_by_rentType(rentTpye=rent_type)
    # 价格筛选
    prices_conditions = re.findall(r'rp([0-9])', conditions)
    if prices_conditions:
        resQ = (resQ & GetQuerying.getQ_by_rp(prices=prices_conditions))
    # 户型筛选
    house_type_conditions = re.findall(r'ht([0-9])', conditions)
    if house_type_conditions:
        resQ = (resQ & GetQuerying.getQ_by_house_tyoe(houseTypes=house_type_conditions))
    # 朝向筛选
    orientation_conditions = re.findall(r'or([0-9])', conditions)
    if orientation_conditions:
        resQ = (resQ & GetQuerying.getQ_by_orientation(orientations=orientation_conditions))
    # 楼层筛选
    floor_conditions = re.findall(r'lc([0-9])', conditions)
    if floor_conditions:
        resQ = (resQ & GetQuerying.getQ_by_floor(floor=floor_conditions))
    # 特色筛选
    tags_conditions = re.findall(r'tg([0-9])',conditions)
    if tags_conditions:
        resQ = (resQ & GetQuerying.getQ_by_tags(tags=tags_conditions))
    # 排序方式
    sorting_condition = re.findall(r'so([0-9])', conditions)
    if sorting_condition:
        sorting_condition = sorting_condition[0]
    else:
        sorting_condition = 2
    page = request.GET.get('page')
    data = get_return_data(city=city,
                           district=district,
                           microdistrict=microdistrict,
                           page=page,
                           resQ=resQ,
                           sort_by=sorting_condition
                           )
    data['current_conditions'] = conditions
    return render(request, 'Mainapp/index2.html', data)


def get_return_data(city, district=None,
                    microdistrict=None,
                    page=None,
                    resQ=None,
                    sort_by=2):
    city_zh = Cities.get(city)
    district_zh = ZH_EN.get(district)
    microdistrict_zh = ZH_EN.get(microdistrict)
    if resQ:
        if microdistrict:
            microdistrict_zh = ZH_EN.get(microdistrict)
            resQ = (resQ & Q(microdistrict=microdistrict_zh))
        elif district:
            resQ = (resQ & Q(district=district_zh))
        result_list = zufang.objects(resQ)
    else:
        if microdistrict:
            result_list = zufang.objects(microdistrict=microdistrict_zh)
        elif district:
            result_list = zufang.objects(district=district_zh)
        else:
            result_list = zufang.objects(city=city_zh)

    if int(sort_by) == SortingWays.Sort_By_Price.value:
        result_list = result_list.order_by('price')
    elif int(sort_by) == SortingWays.Sort_By_Area.value:
        result_list = result_list.order_by('area')

    districts = DM.get(str(city_zh))
    microdistricts = DM.get(str(district_zh))

    total_count = len(result_list)
    paginator = Paginator(result_list, 30)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    data = {
        'contacts': contacts,
        'total_count': total_count,
        'microdistricts': microdistricts,
        'current_city': {'abbr': city, 'zh': city_zh},
        'current_district': {'en': district, 'zh': district_zh},
        'current_microdistrict': microdistrict_zh,
        'districts': districts
    }
    return data


@cache_page(60 * 100)
def find_by_map(request, city):
    city_zh = Cities.get(city)
    data = RentAnalysis.map_count(city_zh)
    data['area'] = District_border.get(city)
    data['city_log'] = City_Center_Point.get(city)[0]
    data['city_lat'] = City_Center_Point.get(city)[1]
    RentAnalysis.map_count(city_zh)
    return render(request, 'Mainapp/map.html', data)









