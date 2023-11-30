from dataclasses import dataclass, field
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime


@dataclass
class ArchetypeId:
    class Meta:
        name = "archetype_id"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Id:
    class Meta:
        name = "id"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "_type",
            "type": "Element",
            "required": True,
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Name:
    class Meta:
        name = "name"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "_type",
            "type": "Element",
            "required": True,
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Origin:
    class Meta:
        name = "origin"

    value: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class StartTime:
    class Meta:
        name = "start_time"

    value: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Subject:
    class Meta:
        name = "subject"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "_type",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class TemplateId:
    class Meta:
        name = "template_id"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class TerminologyId:
    class Meta:
        name = "terminology_id"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "_type",
            "type": "Element",
            "required": True,
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Time:
    class Meta:
        name = "time"

    value: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Value:
    class Meta:
        name = "value"

    type_element: Optional[str] = field(
        default=None,
        metadata={
            "name": "_type",
            "type": "Element",
            "required": True,
        }
    )
    numerator: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    denominator: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    type_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Element",
        }
    )
    magnitude: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    units: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class ArchetypeDetails:
    class Meta:
        name = "archetype_details"

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
    rm_version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class DefiningCode:
    class Meta:
        name = "defining_code"

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


@dataclass
class Encoding:
    class Meta:
        name = "encoding"

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


@dataclass
class ExternalRef:
    class Meta:
        name = "external_ref"

    id: Optional[Id] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    namespace: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
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


@dataclass
class Items:
    class Meta:
        name = "items"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "_type",
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    archetype_node_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    value: Optional[Value] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Language:
    class Meta:
        name = "language"

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


@dataclass
class OtherContext:
    class Meta:
        name = "other_context"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "_type",
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    archetype_node_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    items: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass
class Protocol:
    class Meta:
        name = "protocol"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "_type",
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    archetype_node_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    items: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass
class State:
    class Meta:
        name = "state"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "_type",
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    archetype_node_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    items: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass
class Territory:
    class Meta:
        name = "territory"

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


@dataclass
class Category:
    class Meta:
        name = "category"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    defining_code: Optional[DefiningCode] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Composer:
    class Meta:
        name = "composer"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "_type",
            "type": "Element",
            "required": True,
        }
    )
    external_ref: Optional[ExternalRef] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Events:
    class Meta:
        name = "events"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "_type",
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    archetype_node_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    time: Optional[Time] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    data: Optional["Data"] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    state: Optional[State] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Setting:
    class Meta:
        name = "setting"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    defining_code: Optional[DefiningCode] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Context:
    class Meta:
        name = "context"

    start_time: Optional[StartTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    setting: Optional[Setting] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    other_context: Optional[OtherContext] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Data:
    class Meta:
        name = "data"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "_type",
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    archetype_node_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    origin: Optional[Origin] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    events: List[Events] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    items: List[Items] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Content:
    class Meta:
        name = "content"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "_type",
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    archetype_details: Optional[ArchetypeDetails] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    archetype_node_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    encoding: Optional[Encoding] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    subject: Optional[Subject] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    protocol: Optional[Protocol] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    data: Optional[Data] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Models:
    class Meta:
        name = "models"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "_type",
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    archetype_details: Optional[ArchetypeDetails] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    archetype_node_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    territory: Optional[Territory] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    category: Optional[Category] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    composer: Optional[Composer] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    context: Optional[Context] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    content: List[Content] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
