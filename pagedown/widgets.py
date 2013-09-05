from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.forms.widgets import flatatt
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


class PagedownWidget(forms.Textarea):
    class Media:
        css = {
            'all': ('pagedown/demo/browser/demo.css',)
        }
        js = ('%s/pagedown/Markdown.Converter.js' % settings.STATIC_URL.rstrip('/'),
              '%s/pagedown/Markdown.Sanitizer.js' % settings.STATIC_URL.rstrip('/'),
              '%s/pagedown/Markdown.Editor.js' % settings.STATIC_URL.rstrip('/'),
              'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML',
              '%s/js/mathjax-editing.js' % settings.STATIC_URL,)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        if 'class' not in attrs:
            attrs['class'] = ""
        attrs['class'] += " wmd-input"
        final_attrs = self.build_attrs(attrs, name=name)
        html = """
            <div class="wmd-wrapper">
                <div class="wmd-panel">
                <div id="%(id)s_wmd_button_bar"></div>
                <textarea%(attrs)s>%(body)s</textarea>
                </div>
                <div id="%(id)s_wmd_preview" class="wmd-panel wmd-preview"></div>
            </div>
            <script type="text/javascript">
                (function () {
                    var converter = Markdown.getSanitizingConverter();
                    selectors = {
                        input : "%(id)s",
                        button : "%(id)s_wmd_button_bar",
                        preview : "%(id)s_wmd_preview",
                    }
                    var editor = new Markdown.Editor(converter, "", selectors);
                    var postfix = "";
                    somesquares.mathjaxEditing.prepareWmdForMathJax(editor, postfix, [["$", "$"], ["\\\\\\\\(","\\\\\\\\)"]]);
                    editor.run();
                })();
            </script>
            """ % {
                'attrs': flatatt(final_attrs),
                'body': conditional_escape(force_unicode(value)),
                'id': final_attrs['id'],
            }
        return mark_safe(html)


class AdminPagedownWidget(admin_widgets.AdminTextareaWidget, PagedownWidget):
    class Media:
        css = {
            'all': ('admin/css/pagedown.css',)
        }
