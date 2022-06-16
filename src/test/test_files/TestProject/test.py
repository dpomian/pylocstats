def swap(a, b):
    t = a
    a = b
    b = t
    return a, b


def docstr():
    """
    This is a docstring
    Returns:
    """
    a = 7
    return a*a

def comment():
    a = 3
    l = [2, 3, 4, 9]
    # this is a comment
    result = a in l

    if result:
        x = 7

    # this is another comment
    return min(x, a)

def one_line_docstr():
    """One line doc str"""
    return 42