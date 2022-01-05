from enum import Enum
from typing import Union, Literal, Generic, TypeVar

from pydantic import BaseModel as PBaseModel, validator
from pydantic.generics import GenericModel

StaticPhrasingContent = Union['LineBreak', 'Text']
PhrasingContent = Union['Link', StaticPhrasingContent, "Style"]
FlowContent = Union['Heading', 'Listing', 'ThematicBreak', 'Paragraph', 'Table']
MdastContent = Union[FlowContent, PhrasingContent]
Mdast = Union[MdastContent, "Root"]

MdElement = Union[Mdast, "Row", "Cell", "ListItem"]
ChildrenT = TypeVar('ChildrenT', PhrasingContent, FlowContent, Union[FlowContent, PhrasingContent])

class BaseModel(PBaseModel):

    class Config:
        extra = 'forbid'
        frozen = True

ParentT = TypeVar('ParentT', bound="Parent" )
class Parent(GenericModel, Generic[ChildrenT]):
    children: list[ChildrenT]
    _html_tag = None

    def apply(self: ParentT, fun) -> ParentT:
        return self.copy(
            update={"children": [fun(child) for child in self.children]}
        )

    class Config:
        extra = 'forbid'
        frozen = True

    def inner_to_html(self):
        return " ".join(
            [child.to_html() for child in self.children if child is not None]
        )

    def _to_html(self, html_tag):
        return f"<{html_tag}>{self.inner_to_html()}</{html_tag}>"

    def to_html(self):
        if self._html_tag is None:
            raise Exception(f"Cannot convert to html: {self}")
        return self._to_html(self._html_tag)

    @validator('children', pre=True)
    def ignore_none(cls, v):
        return [child for child in v if child is not None]

class StyleValue(Enum):
    STRIKE = "s"
    STRONG = "strong"
    EMPH = "emph"

class Text(BaseModel):
    text: str
    styles: set[StyleValue] = set()

    @validator('text')
    def strip(cls, text):
        return text.strip(' \n')

    def is_striked(self):
        return StyleValue.STRIKE in self.styles

    def to_html(self):
        return self.text


class Style(Parent[PhrasingContent]):
    type: Literal["Style"] = "Style"
    value: StyleValue

    def to_html(self):
        html_tag = self.value.value
        return self._to_html(html_tag)

class Paragraph(Parent[PhrasingContent]):
    type: Literal["Paragraph"] = "Paragraph"
    _html_tag = "p"

class Link(Parent[StaticPhrasingContent]):
    type: Literal["Link"] = "Link"
    url: str
    title: str

    def to_html(self):
        return f'<link href="{self.url}">{self.inner_to_html()}</link>'

class LineBreak(BaseModel):
    type: Literal["LineBreak"] = "LineBreak"

    def to_html(self):
        return "<br/>"

class ThematicBreak(BaseModel):
    type: Literal["ThematicBreak"] = "ThematicBreak"

    def to_html(self):
        return "<hr>"

class Heading(Parent[PhrasingContent]):
    type: Literal["Heading"] = "Heading"
    level: int

    def to_html(self):
        html_tag = f"h{self.level}"
        return self._to_html(html_tag)

class ListItem(Parent[Union[FlowContent,PhrasingContent]]):
    type: Literal["ListItem"] = "ListItem"
    _html_tag = "li"

class Listing(Parent[Union[ListItem, FlowContent, PhrasingContent]]):
    type: Literal["Listing"] = "Listing"
    _html_tag = "ul"

class Cell(Parent[PhrasingContent]):
    type: Literal["Cell"] = "Cell"
    _html_tag = "td"

class Row(Parent[Cell]):
    type: Literal["Row"] = "Row"
    _html_tag = "tr"

class Table(BaseModel):
    # we allow a cell to be None to preserve table dimensions
    rows : list[list[Union[Cell, PhrasingContent, None]]]
    _html_tag = "table"

    @validator("rows", pre=True)
    def tranform_rows(cls, v):
        res = [
            row.children if isinstance(row, Row) else row
            for row in v
        ]
        return res

    @property
    def children(self):
        return [cell for row in self.rows for cell in row]

    def apply(self, function):
        return Table(rows=[
            [
                function(cell) for cell in row
            ]
            for row in self.rows
        ])

    def to_html(self):
        rows_html = [
            "".join(cell.to_html() for cell in row if cell is not None)
            for row in self.rows
        ]
        inner_html = "".join(
            (f"<tr>{row_html}</tr>" for row_html in rows_html)
        )
        return f"<table>{inner_html}</table>"

    @validator('rows', pre=True)
    def remove_none(cls, v):
        res = []
        for row in v:
            if row is None:
                continue
            if not any(row):
                continue
            res.append(row)
        return res

class Root(Parent[Union[FlowContent, PhrasingContent]]):
    type: Literal["Root"] = "Root"
    _html_tag = "div"

Paragraph.update_forward_refs()
Heading.update_forward_refs()
Link.update_forward_refs()
Listing.update_forward_refs()
ListItem.update_forward_refs()
Table.update_forward_refs()
Cell.update_forward_refs()
Root.update_forward_refs()
Style.update_forward_refs()


