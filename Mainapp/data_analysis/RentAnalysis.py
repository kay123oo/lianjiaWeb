from pyecharts.charts import Bar, Pie, WordCloud
import pandas as pd
from pymongo import MongoClient
from pyecharts import options as opts
from collections import Counter
from operator import itemgetter


class RentAnalysis(object):
    host = '127.0.0.1'
    port = 27017
    db = 'lianjia'

    def __init__(self):
        self.conn = MongoClient(host=self.host, port=self.port)
        self.db = self.conn.get_database(self.db)
        self.zufang_collection = self.db.get_collection('zufang')
        self.mon_data = self.zufang_collection.find()
        self.lianjia_df = pd.DataFrame(list(self.mon_data))
        self.lianjia_df = self.lianjia_df.dropna(subset=['price', 'area'])  # 清理数据，将面积和租金为空的数据去掉
        self.lianjia_df['per_price'] = (self.lianjia_df['price'] / self.lianjia_df['area']).round(decimals=2)

    # 城市各地区房源数量条形图
    def district_house_count(self, city):
        df = self.lianjia_df[self.lianjia_df['city'] == city]
        data = df.groupby('district').count().sort_values(by='price', ascending=False)
        data.sort_values(by='price')
        data_x = data.index
        data_y = list(data.values[:, 0].astype("float"))
        bar = (
            Bar(
                init_opts=opts.InitOpts(
                    width="1000px"
                )
            )
            .add_xaxis(list(data_x))
            .add_yaxis('房源数量', data_y)  # numpy.int32不能显示
            .set_global_opts(title_opts=opts.TitleOpts(title="{}各地区租房房源数量统计".format(city),
                                                       title_textstyle_opts={'color': '#5385c1'}))
        )
        return bar

    # 各地区每平米租金条形图
    def district_rent_price(self, city):
        df = self.lianjia_df[self.lianjia_df['city'] == city]
        apartment_per_price = df[df['dataDistributionType'] == 1].groupby('district')['per_price'].mean().\
            round(decimals=1)
        individual_per_price = df.loc[df['dataDistributionType'] == 0].groupby('district')['per_price'].mean().\
            round(decimals=1)
        df = pd.DataFrame([individual_per_price, apartment_per_price])
        df = df.T
        x_data = list(df.index)
        y1_data = list(df.iloc[:, 0].astype("float"))
        y2_data = list(df.iloc[:, 1].astype("float"))
        bar = (
            Bar(
                init_opts=opts.InitOpts(
                    width="1000px"
                )
            )
            .add_xaxis(x_data)
            .add_yaxis('个人房源', y1_data)  # numpy.int32不能显示
            .add_yaxis('公寓', y2_data)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="{}各地区每平米租金统计".format(city),
                                          title_textstyle_opts={'color': '#5385c1'}),
                yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} 元/平方米")),

            )
        )
        return bar

    # 户型分布
    def house_type_count(self, city):
        temp = self.lianjia_df[self.lianjia_df['city'] == city]
        temp = temp.groupby('houseType')['price'].count().reset_index()
        temp.rename(columns={'price': 'counter'}, inplace=True)
        temp = temp.nlargest(10, 'counter').reset_index()
        x_data = list(temp['houseType'].values)
        y_data = list(temp['counter'].values.astype("float"))
        data_pair = [list(z) for z in zip(x_data, y_data)]
        data_pair.sort(key=lambda x: x[1])
        pie = (
            Pie()
            .add(
                series_name="",
                radius=["50%", "70%"],
                data_pair=[list(z) for z in zip(x_data, y_data)],
                label_opts=opts.LabelOpts(is_show=False, position="center"),
            )
            .set_global_opts(title_opts=opts.TitleOpts(title="{}户型分布".format(city),
                                                       title_textstyle_opts={'color': '#5385c1'},),
                             legend_opts=opts.LegendOpts(type_="scroll",
                                                         pos_left="85%",
                                                         pos_top="20%",
                                                         orient="vertical"),)
            .set_series_opts(
                tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"),
                label_opts=opts.LabelOpts(formatter="{b}:  ({d}%)"))
        )
        return pie

    # 朝向统计
    def orientation_count(self, city):
        temp = self.lianjia_df[self.lianjia_df['city'] == city]
        temp = temp.dropna(subset=['orientation'])  # 清理数据
        temp = temp.groupby('orientation')['price'].count().reset_index()
        temp.rename(columns={'price': 'counter'}, inplace=True)
        temp = temp.nlargest(6, 'counter').reset_index()
        x_data = list(temp['orientation'].values)
        y_data = list(temp['counter'].values.astype("float"))
        data_pair = [list(z) for z in zip(x_data, y_data)]
        data_pair.sort(key=lambda x: x[1])
        pie = (
            Pie(init_opts=opts.InitOpts(width="500px"))
            .add(
                series_name="",
                radius=["40%", "60%"],
                data_pair=data_pair,
                label_opts=opts.LabelOpts(is_show=False, position="center"),
            )
            .set_global_opts(
                legend_opts=opts.LegendOpts(type_="scroll",  pos_top="8%"),
                title_opts=opts.TitleOpts(title="{}朝向统计".format(city),
                                          title_textstyle_opts={'color': '#5385c1'}),


            )
            .set_series_opts(
                tooltip_opts=opts.TooltipOpts(
                    trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
                ),
                label_opts=opts.LabelOpts(formatter="{b}:  ({d}%)")
            )
        )
        return pie

    # 租房面积分布
    def rent_area_count(self, city):
        temp = self.lianjia_df[self.lianjia_df['city'] == city]
        #bins = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 350]
        bins = range(0, 351, 10)
        temp = temp.dropna(subset=['area'])  # 清理数据
        temp['area_group'] = pd.cut(temp.area, bins, right=False)  # 面积分组
        temp = temp.groupby('area_group')['price'].count().reset_index()
        temp.rename(columns={'price': 'counter'}, inplace=True)
        x_data = list(temp['area_group'].values.astype('str'))
        y_data = list(temp['counter'].values.astype("float"))
        bar = (
            Bar(
                init_opts=opts.InitOpts(
                    width="1000px"
                )
            )
            .add_xaxis(x_data)
            .add_yaxis("", y_data)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="{}租房面积统计".format(city),
                                          subtitle="我是副标题",
                                          title_textstyle_opts={'color': '#5385c1'}),
                datazoom_opts=opts.DataZoomOpts(),
                xaxis_opts=opts.AxisOpts(name="单位：㎡"),
            )
        )
        return bar

    # 租金top20商圈
    def microdistrict_price_top10(self, city):
        temp = self.lianjia_df[self.lianjia_df['city'] == city]
        temp = temp.groupby('microdistrict')['per_price'].mean().reset_index()
        temp = temp.round(1)
        temp = temp.nlargest(20, 'per_price').reset_index()
        x_data = list(temp['microdistrict'])
        y_data = list(temp['per_price'])
        bar = (
            Bar(
                init_opts=opts.InitOpts(
                    width="1000px",
                    animation_opts=opts.AnimationOpts(
                        animation_delay=1000, animation_easing="elasticOut"
                    )
                )
            )
            .add_xaxis(x_data)
            .add_yaxis("", y_data)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="{}租金TOP20商圈".format(city),
                                          subtitle="我是副标题",
                                          title_textstyle_opts={'color': '#5385c1'}),
                yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} 元/平方米")),
                datazoom_opts=opts.DataZoomOpts(),
            )

        )
        return bar

    # 标签统计——条形图
    def tags_count_bar(self, city):
        temp = self.lianjia_df[self.lianjia_df['city'] == city]
        tags2 = []
        for tag in temp.dropna(subset=['tags'])['tags']:
            tags2.extend(tag)
        x_data = sorted(Counter(tags2).items(), key=itemgetter(1), reverse=True)
        y_data = sorted(Counter(tags2).items(), key=itemgetter(1), reverse=True)
        x_data = list(map(itemgetter(0), x_data))
        y_data = list(map(itemgetter(1), y_data))
        bar = (
            Bar(
                init_opts=opts.InitOpts(
                    width="1000px"
                )
            )
            .add_xaxis(list(x_data))
            .add_yaxis('', list(y_data))
            .set_global_opts(
                title_opts=opts.TitleOpts(title="{}租房信息标签统计".format(city),
                                          title_textstyle_opts={'color': '#5385c1'}),
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-50)),
            )
        )
        return bar

    # 标签统计——词云
    def tags_count_word_could(self, city):
        temp = self.lianjia_df[self.lianjia_df['city'] == city]
        tags = []
        for tag in temp.dropna(subset=['tags'])['tags']:
            tags.extend(tag)

        for orientation, houseType in zip(temp['orientation'], temp['houseType']):
            tags.append(orientation)
            tags.append(houseType)
        tag_name = Counter(tags).keys()
        tag_count = Counter(tags).values()
        word_cloud = (
            WordCloud()
            .add(series_name="", data_pair=[list(z) for z in zip(tag_name, tag_count)], word_size_range=[6, 66])
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="{}租房标签统计".format(city), title_textstyle_opts={'color': '#5385c1'}
                ),
                tooltip_opts=opts.TooltipOpts(is_show=True),
            )
        )
        return word_cloud

    # 城市租赁类型饼状图
    def rent_type_pie(self, city):
        temp = self.lianjia_df[self.lianjia_df['city'] == city]
        apartment_data = temp[temp['dataDistributionType'] == 1].count()
        entire_rent_data = temp[temp['title'].str.contains('整租')].count()
        joint_rent_data = temp[temp['title'].str.contains('合租')].count()
        y_data = [float(apartment_data[0]), float(entire_rent_data[0]), float(joint_rent_data[0])]
        x_data = ['公寓', '整租', '合租']
        data_pair = [list(z) for z in zip(x_data, y_data)]
        pie = (
            Pie(init_opts=opts.InitOpts(width="500px"))
            .add(
                series_name="",
                radius=["40%", "60%"],
                data_pair=data_pair,
                label_opts=opts.LabelOpts(is_show=False, position="center"),
            )
            .set_global_opts(legend_opts=opts.LegendOpts(type_="scroll", pos_top="8%",),
                             title_opts=opts.TitleOpts(title="{}租赁类型比例".format(city), subtitle="我是副标题",
                                                       title_textstyle_opts={'color': '#5385c1'})
                             )
            .set_series_opts(
                tooltip_opts=opts.TooltipOpts(
                    trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
                ),
                label_opts=opts.LabelOpts(formatter="{b}:  ({d}%)")
            )
        )
        return pie

    # 获取城区、商圈、小区房源数量
    def map_count(self, city):
        temp = self.lianjia_df[self.lianjia_df['city'] == city]
        temp.dropna(subset=['longitude', 'latitude'])
        district_counter = temp.groupby('district').head(1)
        count = temp.groupby('district')['price'].count().astype("str")
        district_counter = district_counter.loc[:, ['district', 'longitude', 'latitude']]
        firstData = pd.merge(district_counter, count, on='district')
        firstData.rename(columns={'price': 'count'}, inplace=True)
        firstData.rename(columns={'district': 'name'}, inplace=True)
        firstData = firstData.to_dict(orient='records')

        microdistrict_counter = temp.groupby('microdistrict').head(1)
        count2 = temp.groupby('microdistrict')['price'].count().astype("str")
        microdistrict_counter = microdistrict_counter.loc[:, ['microdistrict', 'longitude', 'latitude']]
        secondData = pd.merge(microdistrict_counter, count2, on='microdistrict')
        secondData.rename(columns={'price': 'count'}, inplace=True)
        secondData.rename(columns={'microdistrict': 'name'}, inplace=True)
        secondData = secondData.to_dict(orient='records')

        community_counter = temp.groupby('community').head(1)
        count3 = temp.groupby('community')['price'].count().astype("str")
        community_counter = community_counter.loc[:, ['community', 'longitude', 'latitude']]
        thirdData = pd.merge(community_counter, count3, on='community')
        thirdData.rename(columns={'price': 'count'}, inplace=True)
        thirdData.rename(columns={'community': 'name'}, inplace=True)
        thirdData = thirdData.to_dict(orient='records')
        data = {
            "firstData": firstData,
            "secondData": secondData,
            "thirdlyData": thirdData,
        }
        return data


RentAnalysis = RentAnalysis()


