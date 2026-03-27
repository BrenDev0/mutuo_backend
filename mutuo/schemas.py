from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class MutuoSchemaBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        alias_generator=to_camel,
        str_min_length=1,
        str_strip_whitespace=True,
        extra="forbid"
    )