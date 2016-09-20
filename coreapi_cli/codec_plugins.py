import pkg_resources
import collections
import coreapi
import os


def sorting_func(package_info):
    """
    A sorting order for (package, codec_class) tuples. Example ordering:

    application/coreapi+json  (highest priority)
    application/openapi+json  (lower as not a coreapi package built-in)
    application/json          (lower as more general subtype)
    text/*                    (lower as sub type is wildcard)
    */*                       (lowest as main type is wildcard)
    """
    package, codec_class = package_info
    media_type = getattr(codec_class, 'media_type')
    main_type, _, sub_type = media_type.partition('/')
    sub_type = sub_type.split(';')[0]
    is_builtin = package.dist.project_name == 'coreapi'
    return (
        main_type == '*',
        sub_type == '*',
        '+' not in sub_type,
        not is_builtin,
        media_type
    )


def instantiate_codec(cls):
    if issubclass(cls, coreapi.codecs.DownloadCodec):
        default_dir = os.path.join(os.path.expanduser('~'), '.coreapi')
        config_dir = os.environ.get('COREAPI_CONFIG_DIR', default_dir)
        download_dir = os.path.join(config_dir, 'downloads')
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)
        return cls(download_dir=download_dir)
    return cls()


def get_codec_packages():
    """
    Returns a list of (package, codec_class) tuples.
    """
    packages = [
        (package, package.load()) for package in
        pkg_resources.iter_entry_points(group='coreapi.codecs')
    ]
    packages = [
        (package, instantiate_codec(cls)) for (package, cls) in packages
        if issubclass(cls, coreapi.codecs.BaseCodec) or hasattr(cls, 'decode') or hasattr(cls, 'encode')
    ]
    return sorted(packages, key=sorting_func)


def supports(codec):
    """
    Return a list of strings indicating supported operations.
    """
    if hasattr(codec, 'encode') and hasattr(codec, 'decode'):
        return ['encoding', 'decoding']
    elif hasattr(codec, 'encode'):
        return ['encoding']
    elif hasattr(codec, 'decode'):
        return ['decoding']
    # Fallback for pre-2.0 API.
    return codec.supports


codec_packages = get_codec_packages()

codecs = collections.OrderedDict([
    (package.name, codec) for (package, codec) in codec_packages
])

decoders = collections.OrderedDict([
    (package.name, codec) for (package, codec) in codec_packages
    if 'decoding' in supports(codec)
])

encoders = collections.OrderedDict([
    (package.name, codec) for (package, codec) in codec_packages
    if 'encoding' in supports(codec)
])
