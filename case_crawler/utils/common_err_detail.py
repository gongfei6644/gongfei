class TypeSourceError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('没有此类型的网站')