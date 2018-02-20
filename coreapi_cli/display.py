from coreapi.compat import string_types
import coreapi
import json


def display(doc):
    if isinstance(doc, (coreapi.Document, coreapi.Error, coreapi.Object, coreapi.Array, coreapi.Link)):
        codec = coreapi.codecs.DisplayCodec()
        return codec.encode(doc, colorize=True)

    if doc is None:
        return ''

    if isinstance(doc, string_types):
        return doc

    try:
        return json.dumps(doc, indent=4, ensure_ascii=False, separators=coreapi.compat.VERBOSE_SEPARATORS)
    except TypeError:
        return '%s' % doc
