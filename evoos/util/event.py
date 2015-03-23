import json

def digestEvent(event):
    decoded = json.loads(event)
    #DEBUG2
    #print decoded
    eid = decoded["event"] #Event type.
    meta = event
    lid = ""
    if ("lid" in decoded.keys()):
        lid = decoded["lid"]
    
    cbeid = ""
    if ("cbeid" in decoded.keys() and (eid == "addListener" or eid == "removeListener")):
        cbeid = decoded["cbeid"]

    return eid, meta, lid, cbeid
