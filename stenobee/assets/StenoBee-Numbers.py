LONGEST_KEY = 1


MAPPING = str.maketrans("KCDHTPBNRLMV", ".1234567890.", "ZFSQJG$XOI")


NUMBER_KEY = ";"
FORWARDS = "A"
BACKWARDS = "E"

NON_DIGITS = (NUMBER_KEY, FORWARDS, BACKWARDS)


def lookup(stn):
    if len(stn) > 1:
        raise KeyError
    
    stroke = stn[0].replace("-", "")
    if stroke[0] == NUMBER_KEY:
        fwd = FORWARDS in stroke
        bkd = BACKWARDS in stroke
        
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
        stroke = stroke[1:-1]
        
        if not stroke:
            raise KeyError
        
        # Translate to digits
        digits = stroke.translate(MAPPING)
    
        if bkd:
            digits = digits[::-1]

        return "{{&" + "".join(digits) + "}}"
    
    raise KeyError


REV_MAPPING = str.maketrans("1234567890", "CDHTPBNRLM")
NUMERIC = ".1234567890"
DOUBLE_DECIMAL = ";V-AE"


def in_order(prev, curr, desc=False):
    prev.replace("0", ":")
    curr.replace("0", ":")
    if desc:
        return prev > curr
    else:
        return prev < curr


# This only returns one solution based on a greedy algorithm
def reverse_lookup(text):
    buffer = ""
    result = []
    descending = False
    pre_decimal = False
    post_decimal = False
    
    def consume_buffer(dup=False):
        nonlocal buffer, descending, pre_decimal, post_decimal

        keys = buffer.translate(REV_MAPPING)
        if descending:
            pre_decimal, post_decimal = post_decimal, pre_decimal
            keys = keys[::-1]
            suffix = "-E"
        elif dup:
            suffix = "-AE"
        else:
            suffix = "-A"

        if pre_decimal:
            keys = "K" + keys
        if post_decimal:
            keys += "V"
        
        
        result.append(";" + keys + suffix)
        buffer, descending, pre_decimal, post_decimal = ("", False, False, False)

    for c in text:
        if c not in NUMERIC:
            return []
        
        if c == ".":
            if buffer:
                post_decimal = True
                consume_buffer()
            else:
                if pre_decimal:
                    result.append(DOUBLE_DECIMAL)
                    descending, pre_decimal, post_decimal = (False, False, False)
                else:
                    pre_decimal = True
        
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
    
    if buffer or pre_decimal:
        consume_buffer()

    return [tuple(result)]
