# coding: utf8
import difflib

def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return content[:length].rsplit(' ', 1)[0]+suffix
        
def diff(prev_text, next_text, prev_header="Previous", next_header="Next"):
    return difflib.HtmlDiff().make_table(
        prev_text.split('\n'), next_text.split('\n'), prev_header, next_header)\
        .replace("&nbsp;", " ").replace("nowrap=\"nowrap\"","")
        
def timeToText(timeObj):
    return timeObj.strftime("%A, %B %d, %Y %I:%M %p")
