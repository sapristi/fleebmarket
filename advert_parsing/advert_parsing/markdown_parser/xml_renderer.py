from misaka.api import BaseRenderer
from misaka import Markdown
from xml.etree import ElementTree
from xml.sax.saxutils import escape

import logging
logger = logging.getLogger(__name__)


class XMLRenderer(BaseRenderer):
    def blockcode(self, text, language):
        return self.paragraph(self.normal_text(text))
        return text

    def blockquote(self, content):
        return content

    def header(self, content, level):
        return f'<h level="{level}">{content}</h>'

    def hrule(self):
        return '<hrule/>'

    def list(self, content, is_ordered, is_block):
        return f'<list>{content}</list>'

    def listitem(self, content, is_ordered, is_block):
        return f'<li>{content}</li>'

    def paragraph(self, text):
        return f'<p>{text}</p>'

    def table(self, content):
        return f'<table>{content}</table>'

    def table_header(self, content):
        return content

    def table_body(self, content):
        return content

    def table_row(self, content):
        return f'<row>{content}</row>'

    def table_cell(self, text, align, is_header):
        return f'<cell>{text}</cell>'

    def footnotes(self, text):
        return text

    def footnote_def(self, text, number):
        return text

    def footnote_ref(self, number):
        return '<empty/>'

    def blockhtml(self, text):
        return text

    def autolink(self, link, is_email):
        return None

    def codespan(self, text):
        return self.normal_text(text)

    def double_emphasis(self, text):
        return text

    def emphasis(self, text):
        return text

    def underline(self, text):
        return text

    def highlight(self, text):
        return text

    def quote(self, text):
        return text

    def image(self, link, title, alt):
        return '<empty/>'

    def linebreak(self):
        return '<linebreak/>'

    def link(self, content, link, title):
        return content

    def strikethrough(self, text):
        return f'<striked>{text}</striked>'

    def superscript(self, text):
        return text

    def raw_html(self, text):
        return text

    def triple_emphasis(self, text):
        return text

    def math(self, text, displaymode):
        return text

    def normal_text(self, text):
        text = text.strip(' \n')
        if not text:
            return None
        return f'<text>{text}</text>'


def parse_md_to_xml(markdown_str) -> ElementTree.Element:
    markdown_str = markdown_str.replace(
        '\\&#x200B;', '---'
    ).replace(
        '&#x200B;', '---'
    ).replace('', '')
    escaped_md_str = escape(markdown_str).replace('\\>', '>').replace('\\&', '&')

    parser = Markdown(XMLRenderer(), ('tables', 'strikethrough'))
    parsed = parser(escaped_md_str)
    xml_str = f'<root>{parsed}</root>'
    try:
        xml = ElementTree.fromstring(xml_str)
    except Exception as exc:
        logger.error("Parsing failed for xml: %s", xml_str)
        raise exc
    return xml
