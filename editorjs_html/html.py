""" HtmlBlock main Python class"""
import json
import simplejson
import pkg_resources
from django.template import Context, Template

from xblock.core import XBlock
from xblock.fields import Scope, String, Boolean
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader
from xblockutils.settings import XBlockWithSettingsMixin, ThemableXBlockMixin
from xblockutils.studio_editable import StudioEditableXBlockMixin

from .utils import _, DummyTranslationService

loader = ResourceLoader(__name__)

@XBlock.wants('settings')
class HtmlBlock(
    StudioEditableXBlockMixin,
    XBlockWithSettingsMixin,
    ThemableXBlockMixin,
    XBlock
):

    '''
    Icon of the XBlock. Values : [other (default), video, problem]
    '''
    icon_class = "other"

    '''
    Fields
    '''
    display_name = String(
        display_name=_("Display Name"),
        default=_("EditorJs HTML"),
        scope=Scope.settings,
        help=_("This name appears in the horizontal navigation at the top of the page.")
    )

    source_text = String(
        display_name=_("HTML raw content"),
        default='{}',
        scope=Scope.content,
        help=_(
            "This holds json content which requires to load editorjs."
        )
    )

    xblock_html_content = String(
        display_name=_("HTML content"),
        default='',
        scope=Scope.content,
        help=_(
            "This holds HTML content."
        )
    )

    '''
    Util functions
    '''
    def load_resource(self, resource_path):
        """
        Gets the content of a resource
        """
        resource_content = pkg_resources.resource_string(__name__, resource_path)
        return resource_content.decode("utf8")

    def render_template(self, template_path, context={}):
        """
        Evaluate a template by resource path, applying the provided context
        """
        template_str = self.load_resource(template_path)
        return Template(template_str).render(Context(context))

    '''
    Main functions
    '''
    def student_view(self, context=None):
        """
        The primary view of the XBlock, shown to students
        when viewing courses.
        """
        context = {
            'source_text': json.loads(self.source_text),
            'display_name': self.display_name,
            'xblock_html_content': self.xblock_html_content
        }
        html = loader.render_django_template(
            'templates/html/html_view.html',
            context=context
        )

        frag = Fragment(html)
        frag.add_javascript(self.load_resource("static/js/editorjs_html_view.js"))
        frag.add_css(self.load_resource("static/css/styles.css"))
        frag.initialize_js('HtmlXBlockInitView')
        return frag

    def studio_view(self, context=None):
        """
        The secondary view of the XBlock, shown to teachers
        when editing the XBlock.
        """
        context = {
            'source_text': self.source_text,
            'display_name': self.display_name,
            'xblock_html_content': self.xblock_html_content
        }
        html = loader.render_django_template(
            'templates/html/html_edit.html',
            context=context
        )
        frag = Fragment(html)
        frag.add_javascript(self.load_resource("static/js/editorjs_html_edit.js"))
        frag.add_css(self.load_resource("static/css/styles.css"))
        frag.initialize_js('HtmlXBlockInitEdit')
        return frag

    
    @XBlock.json_handler
    def save_html(self, data, suffix=''):
        """
        The saving handler.
        """
        self.source_text = data['source_text']
        self.display_name = data['display_name']
        self.xblock_html_content = self.generate_html(data['source_text'])
        return {
            'result': 'success',
        }

    def generate_html(self, source_text):
        """
        supported elements:
          header
          image
          list
          quote
          warning
          code
          delimiter
          linkTool
          table

        not supported elements
          checklist
          marker
          inlineCode
          embed
          raw
          attaches
        """
        source_text = simplejson.loads(source_text)
        html = '<div class="editorjs-html-content">'
        for block in source_text['blocks']:
              
            if block['type'] == 'header':
                html += '<h'+str(block['data']['level'])+'>'+str(block['data']['text'])+'</h'+str(block['data']['level'])+'>'

            elif block['type'] == 'paragraph':
                html += '<p>'+str(block['data']['text'])+'</p>'

            elif block['type'] == 'list':
                html += '<ul>'
                for item in block['data']['items']:
                    html += '<li>'+str(item)+'</li>'
                html += '</ul>'

            elif block['type'] == 'quote':
                html += '<blockquote>'
                html +=  '<p>'+str(block['data']['text'])+'</p>'
                html +=  '<span class="blockquote-footer">'+str(block['data']['caption'])+'</span>'
                html += '</blockquote>'

            elif block['type'] == 'warning':
                html += '<div class="warning">'
                html += '<strong>'+str(block['data']['title'])+'</strong>'
                html += '<p>'+str(block['data']['message'])+'</p>'
                html += '</div>'

            elif block['type'] == 'code':
                html += '<pre><code>'+str(block['data']['code'])+'</code></pre>'

            elif block['type'] == 'delimiter':
                html += '<hr class="delimiter">'

            elif block['type'] == 'linkTool':
                html += '<a class="resource-link" href="'+str(block['data']['link'])+'">'+str(block['data']['link'])+'</a>'

            elif block['type'] == 'raw':
                html += str(block['data']['html'])
              
            elif block['type'] == 'table':
                html += '<table class="table">'
                html += '<tbody>'
                for element in block['data']['content']:
                    html += '<tr>'
                    for item in element:
                        html += '<td>'
                        html += '<p>'+str(item)+'</p>'
                        html += '</td>'
                    html += '</tr>'
                html += '</tbody>'
                html += '</table>'

            elif block['type'] == 'image':
                html += '<img src="'+str(block['data']['file']['asset_url'])+'">'
                if block['data']['caption']:
                    html += '<span class="caption">'+str(block['data']['caption'])+'</span>'

        html += '</div>'
        return html
