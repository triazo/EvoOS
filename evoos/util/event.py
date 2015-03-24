import json

def digestEvent(event):
    #Breaks down event and cuts out the first four bytes used to calculate the size.
    event = event[4:] 

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
