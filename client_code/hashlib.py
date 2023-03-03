# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import partial

from anvil.js import window

__version__ = "2.2.3"


def digest(algorithm, data):
    """Returns the digest of the data using the specified algorithm.

    Parameters
    ----------
    algorithm : str
        The algorithm to use.
    data : str or bytes
        The data to digest.
    """
    if not isinstance(data, (bytes, str)):
        raise TypeError("data must be a string or bytes object")

    if isinstance(data, str):
        data = data.encode("utf-8")

    hash_buffer = window.crypto.subtle.digest(algorithm, data)
    hash_array = window.Uint8Array(hash_buffer)
    return hash_array.hex()


sha1 = partial(digest, "SHA-1")
sha256 = partial(digest, "SHA-256")
sha384 = partial(digest, "SHA-384")
sha512 = partial(digest, "SHA-512")

if __name__ == "__main__":
    _ = "Hello world!"
    sha1(_)
    sha256(_)
    sha384(_)
    sha512(_)
