# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from functools import partial

from anvil.js import window


def digest(algorithm, data):
    """Returns the digest of the data using the specified algorithm.

    Parameters
    ----------
    algorithm : str
        The algorithm to use.
    data : object
        The data to digest.
    """
    if not isinstance(data, (bytes, str)):
        data = str(data).encode("utf-8")

    if isinstance(data, str):
        data = data.encode("utf-8")

    hash_buffer = window.crypto.subtle.digest(algorithm, data)
    hash_array = window.Uint8Array(hash_buffer)
    return hash_array.hex()


sha1 = partial(digest, algorithm="SHA-1")
sha256 = partial(digest, algorithm="SHA-256")
sha384 = partial(digest, algorithm="SHA-384")
sha512 = partial(digest, algorithm="SHA-512")
