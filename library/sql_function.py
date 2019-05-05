import base64

def object_to_sql(t_object):
    return base64.b64encode(str(t_object).encode('utf-8'))

def sql_to_object(t_sql):
    return eval(base64.b64decode(t_sql).decode())
