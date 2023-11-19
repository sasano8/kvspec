from datetime import datetime, timezone

def wkt_to_geometry(value: str = None):
    if value is None:
        return None
    
    raise Exception()

def geometry_to_wkt(value = None):
    if value is None:
        return None
    
    raise Exception()

def date_to_iso(value: datetime = None):
    if value is None:
        return None
    
    if not isinstance(value, datetime):
        raise Exception("Not datetime object.")
    
    offset = value.utcoffset() 
    if offset is None:
        raise Exception("Naive datetime is not allowed.")
    elif not offset:
        # offset == 0 つまり UTC
        return value.isoformat()
    else:
        return value.astimezone(timezone.utc).isoformat()
    

def date_to_timestamp(value: datetime = None):
    if value is None:
        return None
    
    assert datetime(1,1,2).timestamp() == -62135543939.0
    assert datetime(1,1,1).timestamp() # ValueError: year 0 is out of range

    raise Exception()
    

def iso_to_date(value: str = None):
    if value is None:
        return None
    
    raise Exception()
