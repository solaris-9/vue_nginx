

def generate_select_as_sql(fields, skip=None):
    res = []
    for key in fields.keys():
        if skip:
            if key in skip:
                continue
        
        res.append(
            '`{}` as {}'.format(fields[key]['col'], key)
        )
    return ',\n'.join(res)
    pass

