from dataclasses import dataclass, field
from typing import List, Optional, Union
from xml.etree.ElementTree import QName
from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "http://schemas.openehr.org/v1"


@dataclass(order=True)
class ArchetypeId:
    class Meta:
        name = "archetype_id"
        namespace = "http://schemas.openehr.org/v1"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Existence:
    class Meta:
        name = "existence"
        namespace = "http://schemas.openehr.org/v1"

    lower_included: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper_included: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    lower_unbounded: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper_unbounded: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    lower: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Interval:
    class Meta:
        name = "interval"
        namespace = "http://schemas.openehr.org/v1"

    lower_included: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper_included: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    lower_unbounded: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper_unbounded: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    lower: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Item:
    class Meta:
        name = "item"
        namespace = "http://schemas.openehr.org/v1"

    type_value: Optional[QName] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
            "required": True,
        }
    )
    pattern: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    value: str = field(
        default=""
    )
    list_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "list",
            "type": "Element",
        }
    )


@dataclass(order=True)
class Magnitude:
    class Meta:
        name = "magnitude"
        namespace = "http://schemas.openehr.org/v1"

    lower_included: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper_included: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    lower_unbounded: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper_unbounded: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    lower: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Occurrences:
    class Meta:
        name = "occurrences"
        namespace = "http://schemas.openehr.org/v1"

    lower_included: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper_included: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    lower_unbounded: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper_unbounded: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    lower: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass(order=True)
class OriginalAuthor:
    class Meta:
        name = "original_author"
        namespace = "http://schemas.openehr.org/v1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    value: Union[XmlDate, str] = field(
        default="",
        metadata={
            "required": True,
        }
    )


@dataclass(order=True)
class OtherDetails:
    class Meta:
        name = "other_details"
        namespace = "http://schemas.openehr.org/v1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    value: str = field(
        default=""
    )


@dataclass(order=True)
class Precision:
    class Meta:
        name = "precision"
        namespace = "http://schemas.openehr.org/v1"

    lower_included: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper_included: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    lower_unbounded: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper_unbounded: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    lower: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class TemplateId:
    class Meta:
        name = "template_id"
        namespace = "http://schemas.openehr.org/v1"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class TerminologyId:
    class Meta:
        name = "terminology_id"
        namespace = "http://schemas.openehr.org/v1"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Uid:
    class Meta:
        name = "uid"
        namespace = "http://schemas.openehr.org/v1"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Cardinality:
    class Meta:
        name = "cardinality"
        namespace = "http://schemas.openehr.org/v1"

    is_ordered: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    is_unique: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    interval: Optional[Interval] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Language:
    class Meta:
        name = "language"
        namespace = "http://schemas.openehr.org/v1"

    terminology_id: Optional[TerminologyId] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    code_string: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class LeftOperand:
    class Meta:
        name = "left_operand"
        namespace = "http://schemas.openehr.org/v1"

    type_attribute: Optional[QName] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
            "required": True,
        }
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Element",
            "required": True,
        }
    )
    item: Optional[Item] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    reference_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class ListType:
    class Meta:
        name = "list"
        namespace = "http://schemas.openehr.org/v1"

    magnitude: Optional[Magnitude] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    precision: Optional[Precision] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    units: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Property:
    class Meta:
        name = "property"
        namespace = "http://schemas.openehr.org/v1"

    terminology_id: Optional[TerminologyId] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    code_string: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class RightOperand:
    class Meta:
        name = "right_operand"
        namespace = "http://schemas.openehr.org/v1"

    type_attribute: Optional[QName] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
            "required": True,
        }
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Element",
            "required": True,
        }
    )
    item: Optional[Item] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    reference_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Value:
    class Meta:
        name = "value"
        namespace = "http://schemas.openehr.org/v1"

    terminology_id: Optional[TerminologyId] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    code_string: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Attributes:
    class Meta:
        name = "attributes"
        namespace = "http://schemas.openehr.org/v1"

    type_value: Optional[QName] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
            "required": True,
        }
    )
    rm_attribute_name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    existence: Optional[Existence] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    match_negated: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    children: List["Children"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    cardinality: Optional[Cardinality] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass(order=True)
class Details:
    class Meta:
        name = "details"
        namespace = "http://schemas.openehr.org/v1"

    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Expression:
    class Meta:
        name = "expression"
        namespace = "http://schemas.openehr.org/v1"

    type_attribute: Optional[QName] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
            "required": True,
        }
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Element",
            "required": True,
        }
    )
    operator: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    precedence_overridden: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    left_operand: Optional[LeftOperand] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    right_operand: Optional[RightOperand] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Items:
    class Meta:
        name = "items"
        namespace = "http://schemas.openehr.org/v1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value_simple_type: str = field(
        default=""
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: Optional[Value] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass(order=True)
class Description:
    class Meta:
        name = "description"
        namespace = "http://schemas.openehr.org/v1"

    original_author: List[OriginalAuthor] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    lifecycle_state: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    other_details: List[OtherDetails] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    details: Optional[Details] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Excludes:
    class Meta:
        name = "excludes"
        namespace = "http://schemas.openehr.org/v1"

    string_expression: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    expression: Optional[Expression] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Includes:
    class Meta:
        name = "includes"
        namespace = "http://schemas.openehr.org/v1"

    string_expression: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    expression: Optional[Expression] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class TermBindings:
    class Meta:
        name = "term_bindings"
        namespace = "http://schemas.openehr.org/v1"

    terminology: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    items: List[Items] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass(order=True)
class TermDefinitions:
    class Meta:
        name = "term_definitions"
        namespace = "http://schemas.openehr.org/v1"

    code: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    items: List[Items] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass(order=True)
class Children:
    class Meta:
        name = "children"
        namespace = "http://schemas.openehr.org/v1"

    type_value: Optional[QName] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
            "required": True,
        }
    )
    rm_type_name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    occurrences: Optional[Occurrences] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    node_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    attributes: List[Attributes] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    archetype_id: Optional[ArchetypeId] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    term_definitions: List[TermDefinitions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    term_bindings: Optional[TermBindings] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    property: Optional[Property] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    list_value: Optional[ListType] = field(
        default=None,
        metadata={
            "name": "list",
            "type": "Element",
        }
    )
    includes: Optional[Includes] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    excludes: Optional[Excludes] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    terminology_id: Optional[TerminologyId] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    code_list: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    item: Optional[Item] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass(order=True)
class Definition:
    class Meta:
        name = "definition"
        namespace = "http://schemas.openehr.org/v1"

    rm_type_name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    occurrences: Optional[Occurrences] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    node_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    attributes: List[Attributes] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    archetype_id: Optional[ArchetypeId] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    template_id: Optional[TemplateId] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    term_definitions: List[TermDefinitions] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass(order=True)
class Template:
    class Meta:
        name = "template"
        namespace = "http://schemas.openehr.org/v1"

    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    description: Optional[Description] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    uid: Optional[Uid] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    template_id: Optional[TemplateId] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    concept: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    definition: Optional[Definition] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
