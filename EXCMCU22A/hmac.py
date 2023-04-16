# Implements the hmac module from the Python standard library.


class HMAC:
    def __init__(self, key, msg=None, digestmod=None):
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("key: expected bytes/bytearray")

        import hashlib

        if digestmod is None:
            # TODO: Default hash algorithm is now deprecated.
            digestmod = hashlib.md5

        if callable(digestmod):
            # A hashlib constructor returning a new hash object.
            make_hash = digestmod  # A
        elif isinstance(digestmod, str):
            # A hash name suitable for hashlib.new().
            make_hash = lambda d=b"": hashlib.new(digestmod, d)  # B
        else:
            # A module supporting PEP 247.
            make_hash = digestmod.new  # C

        self._outer = make_hash()
        self._inner = make_hash()

        self.digest_size = getattr(self._inner, "digest_size", None)
        # If the provided hash doesn't support block_size (e.g. built-in
        # has