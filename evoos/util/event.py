import json

def digestEvent(event):
    decoded = json.loads(event)
    #DEBUG2
    print decoded
    eid = decoded["event"] #Event type.
    meta = event
    lid = ""
    if ("lid" in decoded.keys()):
        lid = decoded["lid"]

    return eid, meta, lid
