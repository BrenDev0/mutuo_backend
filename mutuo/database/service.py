from .models import Base

def validate_filters(model: Base, filters: dict):
    for filter in filters.keys():
        if not hasattr(model, filter):
            raise ValueError(f"filter: {filter} not valid for {model.__tablename__}")

