# -*- coding: utf-8 -*-

# gEdit TagBrowser plugin
# Copyright (C) 2012 Fabio Zendhi Nagao
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
import iconlib
import re

def iif(condition, trueVal, falseVal):
    if condition:
        return trueVal
    else:
        return falseVal

class ParserInterface:
    
    def parse(self, doc):
        pass
    
    def cellrenderer(self, tvc, crt, ts, piter):
        pass
    
    def pixbufrenderer(self, tvc, crp, ts, piter):
        crp.set_property("pixbuf", "default")
    

class TagsParser(ParserInterface):
    
    def parse(self, doc):
        code = doc.get_text(*doc.get_bounds())
        tags = self.__generate_tags(code)
        ts = self.__tags_to_ts(tags)
        
        return ts
    
    def cellrenderer(self, tvc, crt, ts, piter):
        text = ts.get_value(piter, 0)
        crt.set_property("foreground-gdk", gtk.gdk.Color(0, 0, 0))
        crt.set_property("text", text)
    
    def pixbufrenderer(self, tvc, crp, ts, piter):
        try:
            icon = ts.get_value(piter, 3)
        except:
            icon = "default"
        crp.set_property("pixbuf", iconlib.pixbufs[icon])
    
    def __generate_tags(self, code):
        tags  = []
        tag   = re.compile("--\[\s*([\S]+)+\s*\]--")

        lines = code.split('\n')
        for i in range(len(lines)):
            line_number  = i + 1
            line_content = lines[i]

            m = tag.search(line_content)
            if m:
                tags.append( ( line_number, m.group(1) ) )

        return tags

    def __tags_to_ts(self, tags):
        ts = gtk.TreeStore(str, str, int, str)
        ts.set_sort_column_id(2, gtk.SORT_ASCENDING)

        scopes = []

        for entry in tags:
            line_number = entry[0]
            path = entry[1].split('.')
            lvl  = len(path) - 1
            scopes = scopes[:lvl]
            tagname = path.pop()
            
            parent = None
            if lvl > 0 and len(scopes) > 0:
                parent = scopes[len(scopes) - 1]

            scopes.append( ts.append(parent , [ tagname, "", line_number, "default" ]) )
        
        return ts
    

# ex:ts=4:et:

