"""\
Code generator functions for wxCalendarCtrl objects

@copyright: 2002-2007 Alberto Griggio
@copyright: 2014-2016 Carsten Grohmann
@license: MIT (see LICENSE.txt) - THIS PROGRAM COMES WITH NO WARRANTY
"""

import common
import wcodegen


class PythonCalendarCtrlGenerator(wcodegen.PythonWidgetCodeWriter):

    tmpl = '%(name)s = %(klass)s(%(parent)s, %(id)s%(style)s)\n'

    import_modules = ['import wx.calendar\n']

    def cn(self, c):
        # TODO remove ugly hack for wxColour
        if c == 'wxColour':
            return wcodegen.PythonWidgetCodeWriter.cn(self, c)
        if c[:2] == 'wx':
            c = c[2:]
        return 'wx.calendar.' + c

    def _prepare_tmpl_content(self, obj):
        wcodegen.PythonWidgetCodeWriter._prepare_tmpl_content(self, obj)
        self.has_setdefault = obj.properties.get('default', False)
        return

# end of class PythonCalendarCtrlGenerator


class CppCalendarCtrlGenerator(wcodegen.CppWidgetCodeWriter):
    import_modules = ['<wx/calctrl.h>']
    tmpl = '%(name)s = new %(klass)s(%(parent)s, %(id)s, wxDefaultDateTime' \
           '%(style)s);\n'

    def _prepare_tmpl_content(self, obj):
        wcodegen.CppWidgetCodeWriter._prepare_tmpl_content(self, obj)
        self.has_setdefault = obj.properties.get('default', False)
        return

# end of class CppCalendarCtrlGenerator


def xrc_code_generator(obj):
    xrcgen = common.code_writers['XRC']

    class CalendarCtrlXrcObject(xrcgen.DefaultXrcObject):
        def write_property(self, name, val, outfile, tabs):
            if name == 'label':
                # translate & into _ as accelerator marker
                val2 = val.replace('&', '_')
                if val.count('&&') > 0:
                    while True:
                        index = val.find('&&')
                        if index < 0:
                            break
                        val = val2[:index] + '&&' + val2[index+2:]
                else:
                    val = val2
            xrcgen.DefaultXrcObject.write_property(self, name, val,
                                                   outfile, tabs)
    # end of class CalendarCtrlXrcObject

    return CalendarCtrlXrcObject(obj)


def initialize():
    klass = 'wxCalendarCtrl'
    common.class_names['EditCalendarCtrl'] = klass
    common.register('python', klass, PythonCalendarCtrlGenerator(klass))
    common.register('C++', klass, CppCalendarCtrlGenerator(klass))
    common.register('XRC', klass, xrc_code_generator)
