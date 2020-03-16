import pypinyin
from django import template
import re

register = template.Library()


@register.simple_tag
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s


@register.simple_tag
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)


@register.simple_tag
def deletestr(arg1, arg2,arg3=None):
    res = re.sub(arg2,'',arg1)
    if arg3:
        res = re.sub(arg3,'',res)
    return res


@register.simple_tag
def delete_and_add(conditions, addstr, deletestr):
    res = re.sub(deletestr, '', conditions)
    return str(res)+str(addstr)
