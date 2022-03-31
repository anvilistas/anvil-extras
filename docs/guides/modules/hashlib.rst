Hashlib
=======
A client module that provides several hashing algorithms.

Usage
-----
The module provides the functions ``sha1``, ``sha256``, ``sha384`` and ``sha512``. Each
can be called by passing the str or bytes object to be hashed and will return a hex string.

e.g.

.. code-block:: python

   from anvil_extras.hashlib import sha256

   print(sha256("Hello World!"))

   >>> 7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069
