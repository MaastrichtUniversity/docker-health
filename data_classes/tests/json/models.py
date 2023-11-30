from dataclasses import dataclass, field
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDate, XmlDuration


@dataclass(order=True)
class Loinc:
    class Meta:
        name = "LOINC"

    at0004_1: Optional[str] = field(
        default=None,
        metadata={
            "name": "at0004.1",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class SnomedCt:
    class Meta:
        name = "SNOMED-CT"

    at0000_1: Optional[str] = field(
        default=None,
        metadata={
            "name": "at0000.1",
            "type": "Element",
            "required": True,
        }
    )
    at0004_1: Optional[str] = field(
        default=None,
        metadata={
            "name": "at0004.1",
            "type": "Element",
            "required": True,
        }
    )
    at0005_1: Optional[str] = field(
        default=None,
        metadata={
            "name": "at0005.1",
            "type": "Element",
            "required": True,
        }
    )
    at0004_2: Optional[str] = field(
        default=None,
        metadata={
            "name": "at0004.2",
            "type": "Element",
            "required": True,
        }
    )
    at0005_2: Optional[str] = field(
        default=None,
        metadata={
            "name": "at0005.2",
            "type": "Element",
            "required": True,
        }
    )
    at0013_1: Optional[str] = field(
        default=None,
        metadata={
            "name": "at0013.1",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Ac01:
    class Meta:
        name = "ac0.1"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    members: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass(order=True)
class Ac02:
    class Meta:
        name = "ac0.2"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    description: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    members: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )


@dataclass(order=True)
class ArchetypeId:
    class Meta:
        name = "archetypeId"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
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


@dataclass(order=True)
class At00001:
    class Meta:
        name = "at0000.1"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass(order=True)
class At00021:
    class Meta:
        name = "at0002.1"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class At00031:
    class Meta:
        name = "at0003.1"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class At00041:
    class Meta:
        name = "at0004.1"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class At00061:
    class Meta:
        name = "at0006.1"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Author:
    class Meta:
        name = "author"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    organisation: Optional[Union[str, XmlDuration]] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass(order=True)
class Cardinality:
    class Meta:
        name = "cardinality"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    interval: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    ordered: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    unique: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Constraint:
    class Meta:
        name = "constraint"

    lower: Optional[Union[int, float, XmlDuration]] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    upper: Optional[Union[int, float, XmlDuration]] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    lower_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "lowerIncluded",
            "type": "Element",
            "required": True,
        }
    )
    upper_included: Optional[bool] = field(
        default=None,
        metadata={
            "name": "upperIncluded",
            "type": "Element",
            "required": True,
        }
    )
    lower_unbounded: Optional[bool] = field(
        default=None,
        metadata={
            "name": "lowerUnbounded",
            "type": "Element",
            "required": True,
        }
    )
    upper_unbounded: Optional[bool] = field(
        default=None,
        metadata={
            "name": "upperUnbounded",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class ConversionDetails:
    class Meta:
        name = "conversionDetails"


@dataclass(order=True)
class IpAcknowledgements:
    class Meta:
        name = "ipAcknowledgements"


@dataclass(order=True)
class LifecycleState:
    class Meta:
        name = "lifecycleState"

    code_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "codeString",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class OriginalAuthor:
    class Meta:
        name = "originalAuthor"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    organisation: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass(order=True)
class OriginalResourceUri:
    class Meta:
        name = "originalResourceUri"


@dataclass(order=True)
class OtherDetails:
    class Meta:
        name = "otherDetails"

    licence: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    custodian_organisation: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_namespace: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_publisher: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    custodian_namespace: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    sem_ver: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    build_uid: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    md5_cam_1_0_1: Optional[str] = field(
        default=None,
        metadata={
            "name": "MD5-CAM-1.0.1",
            "type": "Element",
        }
    )
    parent_md5_cam_1_0_1: Optional[str] = field(
        default=None,
        metadata={
            "name": "PARENT:MD5-CAM-1.0.1",
            "type": "Element",
        }
    )


@dataclass(order=True)
class OtherMetaData:
    class Meta:
        name = "otherMetaData"


@dataclass(order=True)
class References:
    class Meta:
        name = "references"


@dataclass(order=True)
class TerminologyExtracts:
    class Meta:
        name = "terminologyExtracts"


@dataclass(order=True)
class TerminologyId:
    class Meta:
        name = "terminologyId"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class AssumedValue:
    class Meta:
        name = "assumedValue"

    terminology_id: Optional[TerminologyId] = field(
        default=None,
        metadata={
            "name": "terminologyId",
            "type": "Element",
            "required": True,
        }
    )
    code_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "codeString",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Attributes:
    class Meta:
        name = "attributes"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    rm_attribute_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "rmAttributeName",
            "type": "Element",
            "required": True,
        }
    )
    existence: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    cardinality: Optional[Cardinality] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    children: List["Children"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass(order=True)
class Language:
    class Meta:
        name = "language"

    terminology_id: Optional[TerminologyId] = field(
        default=None,
        metadata={
            "name": "terminologyId",
            "type": "Element",
            "required": True,
        }
    )
    code_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "codeString",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Members:
    class Meta:
        name = "members"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    rm_attribute_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "rmAttributeName",
            "type": "Element",
        }
    )
    children: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    rm_type_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "rmTypeName",
            "type": "Element",
        }
    )
    constraint: List[Union[Constraint, str]] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )


@dataclass(order=True)
class OriginalLanguage:
    class Meta:
        name = "originalLanguage"

    terminology_id: Optional[TerminologyId] = field(
        default=None,
        metadata={
            "name": "terminologyId",
            "type": "Element",
            "required": True,
        }
    )
    code_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "codeString",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class TermBindings:
    class Meta:
        name = "termBindings"

    loinc: Optional[Loinc] = field(
        default=None,
        metadata={
            "name": "LOINC",
            "type": "Element",
        }
    )
    snomed_ct: Optional[SnomedCt] = field(
        default=None,
        metadata={
            "name": "SNOMED-CT",
            "type": "Element",
        }
    )


@dataclass(order=True)
class ValueSets:
    class Meta:
        name = "valueSets"

    ac0_1: Optional[Ac01] = field(
        default=None,
        metadata={
            "name": "ac0.1",
            "type": "Element",
        }
    )
    ac0_2: Optional[Ac02] = field(
        default=None,
        metadata={
            "name": "ac0.2",
            "type": "Element",
        }
    )


@dataclass(order=True)
class ArSy:
    class Meta:
        name = "ar-sy"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    copyright: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    ac0_2: Optional[Ac02] = field(
        default=None,
        metadata={
            "name": "ac0.2",
            "type": "Element",
        }
    )
    at0000_1: Optional[At00001] = field(
        default=None,
        metadata={
            "name": "at0000.1",
            "type": "Element",
        }
    )


@dataclass(order=True)
class De:
    class Meta:
        name = "de"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    copyright: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    ac0_2: Optional[Ac02] = field(
        default=None,
        metadata={
            "name": "ac0.2",
            "type": "Element",
        }
    )
    at0000_1: Optional[At00001] = field(
        default=None,
        metadata={
            "name": "at0000.1",
            "type": "Element",
        }
    )


@dataclass(order=True)
class Definition:
    class Meta:
        name = "definition"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    rm_type_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "rmTypeName",
            "type": "Element",
            "required": True,
        }
    )
    node_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "nodeId",
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
    attribute_tuples: List[object] = field(
        default_factory=list,
        metadata={
            "name": "attributeTuples",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass(order=True)
class En:
    class Meta:
        name = "en"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    copyright: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    at0000_1: Optional[At00001] = field(
        default=None,
        metadata={
            "name": "at0000.1",
            "type": "Element",
        }
    )
    ac0_2: Optional[Ac02] = field(
        default=None,
        metadata={
            "name": "ac0.2",
            "type": "Element",
        }
    )
    at0003_1: Optional[At00031] = field(
        default=None,
        metadata={
            "name": "at0003.1",
            "type": "Element",
        }
    )
    at0004_1: Optional[At00041] = field(
        default=None,
        metadata={
            "name": "at0004.1",
            "type": "Element",
        }
    )
    at0002_1: Optional[At00021] = field(
        default=None,
        metadata={
            "name": "at0002.1",
            "type": "Element",
        }
    )
    at0006_1: Optional[At00061] = field(
        default=None,
        metadata={
            "name": "at0006.1",
            "type": "Element",
        }
    )


@dataclass(order=True)
class Es:
    class Meta:
        name = "es"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    copyright: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    ac0_2: Optional[Ac02] = field(
        default=None,
        metadata={
            "name": "ac0.2",
            "type": "Element",
        }
    )
    at0000_1: Optional[At00001] = field(
        default=None,
        metadata={
            "name": "at0000.1",
            "type": "Element",
        }
    )


@dataclass(order=True)
class EsAr:
    class Meta:
        name = "es-ar"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    copyright: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    at0000_1: Optional[At00001] = field(
        default=None,
        metadata={
            "name": "at0000.1",
            "type": "Element",
        }
    )


@dataclass(order=True)
class EsCo:
    class Meta:
        name = "es-co"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    copyright: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    ac0_2: Optional[Ac02] = field(
        default=None,
        metadata={
            "name": "ac0.2",
            "type": "Element",
        }
    )


@dataclass(order=True)
class Fa:
    class Meta:
        name = "fa"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    copyright: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )


@dataclass(order=True)
class Fi:
    class Meta:
        name = "fi"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    ac0_2: Optional[Ac02] = field(
        default=None,
        metadata={
            "name": "ac0.2",
            "type": "Element",
        }
    )
    at0000_1: Optional[At00001] = field(
        default=None,
        metadata={
            "name": "at0000.1",
            "type": "Element",
        }
    )


@dataclass(order=True)
class Fr:
    class Meta:
        name = "fr"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    at0000_1: Optional[At00001] = field(
        default=None,
        metadata={
            "name": "at0000.1",
            "type": "Element",
        }
    )


@dataclass(order=True)
class It:
    class Meta:
        name = "it"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    at0000_1: Optional[At00001] = field(
        default=None,
        metadata={
            "name": "at0000.1",
            "type": "Element",
        }
    )


@dataclass(order=True)
class Ja:
    class Meta:
        name = "ja"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    copyright: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )


@dataclass(order=True)
class Ko:
    class Meta:
        name = "ko"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    copyright: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    at0000_1: Optional[At00001] = field(
        default=None,
        metadata={
            "name": "at0000.1",
            "type": "Element",
        }
    )


@dataclass(order=True)
class Nb:
    class Meta:
        name = "nb"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    ac0_2: Optional[Ac02] = field(
        default=None,
        metadata={
            "name": "ac0.2",
            "type": "Element",
        }
    )
    at0000_1: Optional[At00001] = field(
        default=None,
        metadata={
            "name": "at0000.1",
            "type": "Element",
        }
    )


@dataclass(order=True)
class Nl:
    class Meta:
        name = "nl"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    copyright: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    ac0_2: Optional[Ac02] = field(
        default=None,
        metadata={
            "name": "ac0.2",
            "type": "Element",
        }
    )
    at0000_1: Optional[At00001] = field(
        default=None,
        metadata={
            "name": "at0000.1",
            "type": "Element",
        }
    )


@dataclass(order=True)
class PtBr:
    class Meta:
        name = "pt-br"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    copyright: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    ac0_2: Optional[Ac02] = field(
        default=None,
        metadata={
            "name": "ac0.2",
            "type": "Element",
        }
    )
    at0000_1: Optional[At00001] = field(
        default=None,
        metadata={
            "name": "at0000.1",
            "type": "Element",
        }
    )


@dataclass(order=True)
class Ru:
    class Meta:
        name = "ru"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    copyright: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    ac0_2: Optional[Ac02] = field(
        default=None,
        metadata={
            "name": "ac0.2",
            "type": "Element",
        }
    )


@dataclass(order=True)
class Sv:
    class Meta:
        name = "sv"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )
    ac0_2: Optional[Ac02] = field(
        default=None,
        metadata={
            "name": "ac0.2",
            "type": "Element",
        }
    )
    at0000_1: Optional[At00001] = field(
        default=None,
        metadata={
            "name": "at0000.1",
            "type": "Element",
        }
    )


@dataclass(order=True)
class Translations:
    class Meta:
        name = "translations"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
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
    author: Optional[Author] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    accreditation: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class Tuples:
    class Meta:
        name = "tuples"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    members: List[Members] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass(order=True)
class ZhCn:
    class Meta:
        name = "zh-cn"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    keywords: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    use: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    misuse: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    copyright: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    original_resource_uri: Optional[OriginalResourceUri] = field(
        default=None,
        metadata={
            "name": "originalResourceUri",
            "type": "Element",
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
        }
    )


@dataclass(order=True)
class AttributeTuples:
    class Meta:
        name = "attributeTuples"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    members: List[Members] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    tuples: List[Tuples] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass(order=True)
class Details:
    class Meta:
        name = "details"

    de: Optional[De] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    ru: Optional[Ru] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    sv: Optional[Sv] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    fi: Optional[Fi] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    ko: Optional[Ko] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    pt_br: Optional[PtBr] = field(
        default=None,
        metadata={
            "name": "pt-br",
            "type": "Element",
            "required": True,
        }
    )
    ar_sy: Optional[ArSy] = field(
        default=None,
        metadata={
            "name": "ar-sy",
            "type": "Element",
            "required": True,
        }
    )
    en: Optional[En] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    it: Optional[It] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    fr: Optional[Fr] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    zh_cn: Optional[ZhCn] = field(
        default=None,
        metadata={
            "name": "zh-cn",
            "type": "Element",
        }
    )
    es: Optional[Es] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    es_ar: Optional[EsAr] = field(
        default=None,
        metadata={
            "name": "es-ar",
            "type": "Element",
        }
    )
    nb: Optional[Nb] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    ja: Optional[Ja] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    fa: Optional[Fa] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    nl: Optional[Nl] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    es_co: Optional[EsCo] = field(
        default=None,
        metadata={
            "name": "es-co",
            "type": "Element",
        }
    )


@dataclass(order=True)
class TermDefinitions:
    class Meta:
        name = "termDefinitions"

    es_co: Optional[EsCo] = field(
        default=None,
        metadata={
            "name": "es-co",
            "type": "Element",
        }
    )
    en: Optional[En] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    ja: Optional[Ja] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    de: Optional[De] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    zh_cn: Optional[ZhCn] = field(
        default=None,
        metadata={
            "name": "zh-cn",
            "type": "Element",
        }
    )
    nl: Optional[Nl] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    ru: Optional[Ru] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    fa: Optional[Fa] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    ar_sy: Optional[ArSy] = field(
        default=None,
        metadata={
            "name": "ar-sy",
            "type": "Element",
            "required": True,
        }
    )
    es_ar: Optional[EsAr] = field(
        default=None,
        metadata={
            "name": "es-ar",
            "type": "Element",
        }
    )
    pt_br: Optional[PtBr] = field(
        default=None,
        metadata={
            "name": "pt-br",
            "type": "Element",
            "required": True,
        }
    )
    ko: Optional[Ko] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    es: Optional[Es] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    nb: Optional[Nb] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    sv: Optional[Sv] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    fi: Optional[Fi] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    it: Optional[It] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    fr: Optional[Fr] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass(order=True)
class Children:
    class Meta:
        name = "children"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    rm_type_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "rmTypeName",
            "type": "Element",
        }
    )
    occurrences: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    node_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "nodeId",
            "type": "Element",
        }
    )
    target_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "targetPath",
            "type": "Element",
        }
    )
    attributes: List[Attributes] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    attribute_tuples: List[AttributeTuples] = field(
        default_factory=list,
        metadata={
            "name": "attributeTuples",
            "type": "Element",
        }
    )
    archetype_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "archetypeRef",
            "type": "Element",
        }
    )
    reference_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "referenceType",
            "type": "Element",
        }
    )
    assumed_value: Optional[AssumedValue] = field(
        default=None,
        metadata={
            "name": "assumedValue",
            "type": "Element",
        }
    )
    terminology_id: Optional[TerminologyId] = field(
        default=None,
        metadata={
            "name": "terminologyId",
            "type": "Element",
        }
    )
    constraint: List[Union[str, int, Constraint]] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    selected_terminologies: List[object] = field(
        default_factory=list,
        metadata={
            "name": "selectedTerminologies",
            "type": "Element",
        }
    )


@dataclass(order=True)
class Description:
    class Meta:
        name = "description"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    original_author: Optional[OriginalAuthor] = field(
        default=None,
        metadata={
            "name": "originalAuthor",
            "type": "Element",
            "required": True,
        }
    )
    other_contributors: List[object] = field(
        default_factory=list,
        metadata={
            "name": "otherContributors",
            "type": "Element",
            "min_occurs": 1,
        }
    )
    lifecycle_state: Optional[LifecycleState] = field(
        default=None,
        metadata={
            "name": "lifecycleState",
            "type": "Element",
        }
    )
    ip_acknowledgements: Optional[IpAcknowledgements] = field(
        default=None,
        metadata={
            "name": "ipAcknowledgements",
            "type": "Element",
            "required": True,
        }
    )
    references: Optional[References] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    conversion_details: Optional[ConversionDetails] = field(
        default=None,
        metadata={
            "name": "conversionDetails",
            "type": "Element",
            "required": True,
        }
    )
    other_details: Optional[OtherDetails] = field(
        default=None,
        metadata={
            "name": "otherDetails",
            "type": "Element",
            "required": True,
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
class Terminology:
    class Meta:
        name = "terminology"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    concept_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "conceptCode",
            "type": "Element",
            "required": True,
        }
    )
    term_definitions: Optional[TermDefinitions] = field(
        default=None,
        metadata={
            "name": "termDefinitions",
            "type": "Element",
            "required": True,
        }
    )
    term_bindings: Optional[TermBindings] = field(
        default=None,
        metadata={
            "name": "termBindings",
            "type": "Element",
            "required": True,
        }
    )
    terminology_extracts: Optional[TerminologyExtracts] = field(
        default=None,
        metadata={
            "name": "terminologyExtracts",
            "type": "Element",
            "required": True,
        }
    )
    value_sets: Optional[ValueSets] = field(
        default=None,
        metadata={
            "name": "valueSets",
            "type": "Element",
            "required": True,
        }
    )


@dataclass(order=True)
class TemplateOverlays:
    class Meta:
        name = "templateOverlays"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    uid: Optional[str] = field(
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
    parent_archetype_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "parentArchetypeId",
            "type": "Element",
            "required": True,
        }
    )
    differential: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    archetype_id: Optional[ArchetypeId] = field(
        default=None,
        metadata={
            "name": "archetypeId",
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
    terminology: Optional[Terminology] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    adl_version: Optional[float] = field(
        default=None,
        metadata={
            "name": "adlVersion",
            "type": "Element",
            "required": True,
        }
    )
    build_uid: Optional[str] = field(
        default=None,
        metadata={
            "name": "buildUid",
            "type": "Element",
            "required": True,
        }
    )
    rm_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "rmName",
            "type": "Element",
            "required": True,
        }
    )
    rm_release: Optional[str] = field(
        default=None,
        metadata={
            "name": "rmRelease",
            "type": "Element",
            "required": True,
        }
    )
    generated: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    other_meta_data: Optional[OtherMetaData] = field(
        default=None,
        metadata={
            "name": "otherMetaData",
            "type": "Element",
            "required": True,
        }
    )
    original_language: Optional[OriginalLanguage] = field(
        default=None,
        metadata={
            "name": "originalLanguage",
            "type": "Element",
            "required": True,
        }
    )
    translations: List[Translations] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass(order=True)
class Models:
    class Meta:
        name = "models"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "@type",
            "type": "Element",
            "required": True,
        }
    )
    uid: Optional[str] = field(
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
    parent_archetype_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "parentArchetypeId",
            "type": "Element",
            "required": True,
        }
    )
    differential: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    archetype_id: Optional[ArchetypeId] = field(
        default=None,
        metadata={
            "name": "archetypeId",
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
    terminology: Optional[Terminology] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    adl_version: Optional[float] = field(
        default=None,
        metadata={
            "name": "adlVersion",
            "type": "Element",
            "required": True,
        }
    )
    build_uid: Optional[str] = field(
        default=None,
        metadata={
            "name": "buildUid",
            "type": "Element",
            "required": True,
        }
    )
    rm_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "rmName",
            "type": "Element",
            "required": True,
        }
    )
    rm_release: Optional[str] = field(
        default=None,
        metadata={
            "name": "rmRelease",
            "type": "Element",
            "required": True,
        }
    )
    generated: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    template_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "templateId",
            "type": "Element",
            "required": True,
        }
    )
    other_meta_data: Optional[OtherMetaData] = field(
        default=None,
        metadata={
            "name": "otherMetaData",
            "type": "Element",
            "required": True,
        }
    )
    template_overlays: List[TemplateOverlays] = field(
        default_factory=list,
        metadata={
            "name": "templateOverlays",
            "type": "Element",
            "min_occurs": 1,
        }
    )
    original_language: Optional[OriginalLanguage] = field(
        default=None,
        metadata={
            "name": "originalLanguage",
            "type": "Element",
            "required": True,
        }
    )
    translations: List[Translations] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
