def shorten(sam: list) -> list:
    """Convert long format of cs tag into short format

    Args:
        sam (list): List of SAM (Sequence Alignment/Map Format) including a cs tag in **long** form

    Returns:
        List of SAM including a cs tag in **short** form

    Example:
        >>> import cstag
        >>> sam = [hoge]
        >>> cstag.shorten(sam)
        [hoge]
    """
    print("Hello!!")

def lengthen(sam: list) -> list:
    """Convert short format of cs tag into long format
    Args:
        sam (list): List of SAM (Sequence Alignment/Map Format) including a cs tag in **short** form

    Returns:
        List of SAM including a cs tag in **long** form

    Example:
        >>> import cstag
        >>> sam = [hoge]
        >>> cstag.lengthen(sam)
        [hoge]
    """
    print("こんにちは")
