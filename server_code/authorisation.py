# MIT License
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This software is published at https://github.com/anvilistas/anvil-extras
import functools

import anvil.users

__version__ = "1.1.0"


def authentication_required(func):
    """A decorator to ensure only a valid user can call a server function"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if anvil.users.get_user() is None:
            raise ValueError("Authentication required")
        else:
            return func(*args, **kwargs)

    return wrapper


def authorisation_required(permissions):
    """A decorator to ensure a user has sufficient permissions to call a server function"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = anvil.users.get_user()
            if user is None:
                raise ValueError("Authentication required")
            if isinstance(permissions, str):
                required_permissions = set([permissions])
            else:
                required_permissions = set(permissions)
            try:
                user_permissions = set(
                    [
                        permission["name"]
                        for role in user["roles"]
                        for permission in role["permissions"]
                    ]
                )
            except TypeError:
                raise ValueError("Authorisation required")

            if not required_permissions.issubset(user_permissions):
                raise ValueError("Authorisation required")
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator
