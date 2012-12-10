# coding=gbk

def GetUnicodeFromString(str_str):
    str_str = unicode(str_str)
    str_uni = ""
    for char in str_str:
        char_uni = str(hex(ord(char)))
        str_uni += char_uni
    return str_uni
        
print GetUnicodeFromString("中a")       