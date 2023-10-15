LONGEST_KEY = 1


MAPPING = str.maketrans("KMHTJQNDFB", "1234567890")

NON_NUMBER_KEY = list("^XPSLCRGV")
DECIMAL_KEY = "Z"
FORWARDS = "A"
BACKWARDS = "E"

def lookup(stn):
    if len(stn) > 1:
        raise KeyError
    
    stroke = stn[0].replace("-", "")

    if any(key in stroke for key in NON_NUMBER_KEY):
        raise KeyError

    if "A*" in stroke or "*E" in stroke:
        fwd = FORWARDS in stroke
        bkd = BACKWARDS in stroke
        dot = DECIMAL_KEY in stroke
        
        if fwd == bkd:
            if fwd and bkd:
                keys = "".join(key for key in stroke if ord(key) in MAPPING)
                digits = keys.translate(MAPPING)
                if len(digits) == 1:
                    return "{&" + digits * 2 + "}"
                
            raise KeyError
        
        if any(MAPPING.get(ord(key), "") is None for key in stroke):
            raise KeyError
        
        # We know that the first key is ; and the last key is EI
        # because we checked, so now that we don't need them we
        # can just remove them
        stroke = "".join(key for key in stroke if ord(key) in MAPPING)
        
        if not stroke:
            raise KeyError
        
        # Translate to digits
        digits = stroke.translate(MAPPING)
    
        if bkd:
            digits = digits[::-1]
        return "{&" + "".join(digits) + (dot * ".") + "}"

    raise KeyError


REV_MAPPING = str.maketrans("1234567890", "KMHTJQNDFB")
NUMERIC = ".1234567890"


def in_order(prev, curr, desc=False):
    prev = prev.replace("0", ":")
    curr = curr.replace("0", ":")
    if desc:
        return prev > curr
    else:
        return prev < curr


# This only returns one solution based on a greedy algorithm
def reverse_lookup(text):
    buffer = ""
    result = []
    descending = False
    append_decimal = False
    
    def consume_buffer(dup=False):
        nonlocal buffer, descending, append_decimal
        keys = buffer.translate(REV_MAPPING)
        if descending:
            # pre_decimal, post_decimal = post_decimal, pre_decimal
            keys = keys[::-1]
            suffix = "-*E"
        elif dup:
            suffix = "-A*E"
        else:
            suffix = "-A*"

        if append_decimal:
            keys = "Z" + keys

        result.append(keys + suffix)
        buffer, descending, append_decimal = ("", False, False)

    for c in text:
        if c not in NUMERIC:
            return []
        
        if c == ".":
            append_decimal = True
            consume_buffer()
        
        elif c.isdigit():
            if len(buffer) > 1:
                if in_order(buffer[-1], c, descending):
                    buffer += c
                else:
                    consume_buffer()
                    buffer = c
            elif len(buffer) == 1:
                if c == buffer:
                    consume_buffer(True)
                    continue
                
                if not in_order(buffer, c):
                    descending = True
                
                buffer += c
            
            else:
                buffer = c
    
    if buffer:
        consume_buffer()

    return [tuple(result)]
