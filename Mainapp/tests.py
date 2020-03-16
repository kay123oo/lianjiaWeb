
   # microdistricts = zufang.objects.item_frequencies("microdistrict").keys()
   # for microdistrict in microdistricts:
   #     en = pinyin(microdistrict)
   #     ZH_EN[en] = microdistrict
   #     res = str("\'{}\':\'{}\',").format(en,microdistrict)
   #     print(res)


import re

lc = re.findall(r'lc([0-9])', "lc2f1rp1rp2lc3f4")
f1 = re.findall(r'f([0-9])', "lc2f1rp1rp2lc3f4")
rp = re.findall(r'rp([0-9])', "lc2f1rp1rp2lc3f4")
print(lc)
print(f1)
print(rp)
