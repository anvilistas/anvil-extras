Routing
=======

The routing module allows hash-based navigation in an Anvil app.

+---------------------------------------+-------------------------------------------------------------------------------------------+
| Live Example:                         | `hash-routing-example.anvil.app <https://hash-routing-example.anvil.app/>`__              |
+---------------------------------------+-------------------------------------------------------------------------------------------+
| Example Clone Link:                   | `Example <https://anvil.works/build#clone:JVKXENWGKTU6IO7Y=O62PB7QCYEEU4ZBDTJQ6V6W4>`__   |
+---------------------------------------+-------------------------------------------------------------------------------------------+


Introduction
------------

An Anvil app is a single-page app. When the user navigates through the app's pages the URL does not change.
The part of the URL before the `#` is used by the server to identify the app.
The part following the `#`, is never sent to the server and used only by the browser.

The routing module takes advantage of the URL hash and allows unique URLs to be defined for forms within an app.
Here are a few examples of URL hashes within an app and associated terminology.

+--------------------------------+----------------------+-----------------+-----------------+--------------+-----------------+
| URL                            | ``url_hash``         | ``url_pattern`` | ``url_dict``    | ``url_keys`` | ``dynamic_vars``|
+================================+======================+=================+=================+==============+=================+
| ``blog.anvil.app/#``           | ``''``               | ``''``          | ``{}``          |  ``[]``      | ``{}``          |
+--------------------------------+----------------------+-----------------+-----------------+--------------+-----------------+
| ``blog.anvil.app/#blog``       | ``'blog'``           | ``'blog'``      | ``{}``          | ``[]``       | ``{}``          |
+--------------------------------+----------------------+-----------------+-----------------+--------------+-----------------+
| ``blog.anvil.app/#blog?id=10`` | ``'blog?id=10'``     | ``'blog'``      | ``{'id':'10'}`` | ``['id']``   | ``{}``          |
+--------------------------------+----------------------+-----------------+-----------------+--------------+-----------------+
| ``blog.anvil.app/#blog/10``    | ``'blog/10'``        | ``'blog/{id}'`` | ``{}``          | ``[]``       | ``{'id': 10}``  |
+--------------------------------+----------------------+-----------------+-----------------+--------------+-----------------+


Main Form
---------

This is either the startup form or the form loaded from a startup module.
It contains the header, the navigation bar and a ``content_panel``.
It is based on the Material Design standard-page.html.

The ``MainForm`` is **not** the ``HomeForm``. The ``MainForm`` has **no
content**. It only has a navigation bar, header, optional sidebar and a ``content_panel``.

-  import the routing module
-  import all the forms that may be added to the ``content_panel``
-  add the decorator: ``@routing.main_router``

.. code:: python

    from anvil_extras import routing
    from .Form1 import Form1
    from .Form2 import Form2
    from .Form3 import Form3
    from .ErrorForm import ErrorForm

    @routing.main_router
    class Main(MainTemplate):



Route Forms
-----------

A route form is any form that will be loaded inside the ``MainForm``'s
``content_panel``.

-  Import the routing module
-  add the ``@routing.route`` decorator above the class definition
-  The first argument to the decorator is the ``url_pattern``
   (think of it as the page name).
-  The second argument is optional and is any ``url_keys``
   (a list of strings that make up a query strings in the ``url_hash``)

.. code:: python

    from anvil_extras import routing

    @routing.route('article', url_keys=['id'])
    class ArticleForm(ArticleFormTemplate):
        ...


Or without any ``url_keys``


.. code:: python

    from anvil_extras import routing

    @routing.route('article')
    class ArticleForm(ArticleFormTemplate):
        ...


Home form
---------

The ``HomeForm`` is also a ``Route Form`` that appears in the ``content_panel`` of the ``MainForm``.

-  Import the routing module
-  add the ``@routing.route`` decorator
-  set the ``url_pattern`` (page name) to an empty string

.. code:: python

    from anvil_extras import routing

    @routing.route('')
    class Home(HomeTemplate):
        ...

--------------

Error form (Optional)
---------------------

This is the form that is shown when the ``url_hash`` refers to a page
that does not exist, or the query string does not match the ``url_keys``
listed in the decorator. Follow these steps to create an error form that
shows an error message:

-  Create a form with the label ``Sorry, this page does not exist``
-  Import the routing module
-  add the decorator ``@routing.error_form``

.. code:: python

    from anvil_extras import routing

    @routing.error_form
    class ErrorForm(ErrorFormTemplate):
        ...

--------------

Navigation
----------

It is important to never use the typical method to navigate when
using the ``routing`` module.

.. code:: python

    # Banned
    get_open_form().content_panel.clear()
    get_open_form().content_panel.add_component(Form1())
    # This will result in an Exception('Form1 is a route form and was not loaded from routing')

Instead

.. code:: python

    # option 1
    set_url_hash('articles') # anvil's built in method

    # or an empty string to navigate to the home page
    set_url_hash('')

    # option 2
    routing.set_url_hash('articles')
    #routing.set_url_hash() method has some bonus features.


With query string parameters:

.. code:: python

    # option 1
    set_url_hash(f'article?id={self.item["id"]}')

    # option 2
    routing.set_url_hash(f'article?id={self.item["id"]}')

    # option 3
    routing.set_url_hash(url_pattern='article', url_dict={'id':self.item['id']})


``routing.set_url_hash()`` - has some additional features.
See `API Docs <#api>`__ and Examples.



Dynamic Vars
------------

An alternative to a query string is to include a dynamic URL hash.
The dynamic variables inside the URL pattern will be included in the ``dynamic_vars`` attribute.

.. code:: python

    from anvil_extras import routing

    @routing.route("article/{id}")
    class ArticleForm(ArticleFormTemplate):
        ...

You can then check the ``id`` using:

.. code:: python

        print(self.dynamic_vars) # {'id': 3}
        print(self.dynamic_vars['id']) # 3

Multiple dynanamic variables are supported e.g. ``foo/{var_name_1}/{var_name_2}``.
A dynamic varaible must be entirely contained within a ``/`` portion of the ``url_pattern``,
e.g. ``foo/article-{id}`` is not valid.

--------------


API
---

Decorators
^^^^^^^^^^
.. attribute:: routing.main_router

    Apply this decorator above the top-level Form - ``MainForm``.
    The ``MainForm`` must have a ``content_panel``.
    There are two callbacks available to a ``main_router`` ``MainForm``.

    .. method:: on_navitagion(self, **nav_args)
                on_navitagion(self, url_hash, url_patter, url_dict, unload_form)

        The ``on_navigation`` method, when added to your ``MainForm``, will be called whenever the ``url_hash`` is changed.
        It's a good place to adjust the look of your ``MainForm`` if the ``url_hash`` changes. e.g. the selected link in the sidebar.
        The ``unload_form`` is possible ``None`` if this is the first load of the app.

    .. method:: on_form_load(self, **nav_args)
                on_form_load(self, url_hash, url_patter, url_dict, form)

        The ``on_form_load`` is called after a form has been loaded into the ``content_panel``.
        This is also a good time to adjust the ``MainForm``.


.. function:: routing.route(url_pattern, url_keys=[], title=None, full_width_row=False)

    The ``routing.route`` decorator should be called with arguments that determine the shape of the ``url_hash``.
    The ``url_pattern`` determines the string immediately after the ``#``.
    The ``url_keys`` determine the required query string parameters in a ``url_hash``.

    The routing module adds certain parameters to a ``Route Form`` and supports a ``before_unload`` callback.

    .. attribute:: url_hash

        The current ``url_hash``. The ``url_hash`` includes the query. See `Introduction <#introduction>`__ for examples.

    .. attribute:: url_pattern

        The ``url_hash`` without the query string.

    .. attribute:: url_dict

        The query string converted to a python dict.

    .. attribute:: dynamic_vars

        See `Dynamic URLs <#dynamic-urls>`__.

    .. method:: before_unload(self)

        If the ``before_unload`` method is added it will be called whenever the form currently in the ``content_panel`` is about to be removed.
        If any truthy value is returned then unloading will be prevented. See `Form Unloading <#form-unloading>`__.

.. attribute:: routing.error_form

    The ``routing.error_form`` decorator is optional and can be added above a form
    that will be displayed if the ``url_hash`` does not refer to any known ``Route Form``.



List of Methods
^^^^^^^^^^^^^^^

.. function:: routing.set_url_hash(url_hash)
              routing.set_url_hash(url_hash, **properties)
              routing.set_url_hash(url_pattern=None, url_dict=None, **properties)
              routing.set_url_hash(url_hash, *, replace_current_url=False, set_in_history=True, redirect=True, load_from_cache=True, **properties)

    Sets the ``url_hash`` and begins navigation to load a form. Any properties provided will be passed to the form's properties.
    You can also pass the url_pattern and url_dict separately and let the routing module convert this to a valid url_hash.
    This is particularly useful when you have strings that need encoding as part of the query string.

    The additional keywords in the call signature will adjust the routing behaviour.

    If ``replace_current_url`` is set to ``True``. Then the navigation will happen "in place" rather than as a new history item.

    If ``set_in_history`` is set to ``False`` the URL will not be added to the browser's history stack.

    If ``redirect`` is set to ``False`` then you do not want to navigate away from the current form.

    if ``load_from_cache`` is set to ``False`` then the new URL will **not** load from cache.

    Note that any additional properties will only be passed to a form
    if it is the first time the form has loaded and/or it is **not** loaded from cache.


.. function:: routing.get_url_components(url_hash=None)

    Returns a 3 tuple of the ``url_hash``, ``url_pattern`` and ``url_dict``.
    If the ``url_hash`` is None it will return the components based on the current ``url_hash`` of the page.

.. function:: routing.get_url_hash(url_hash=None)

    Returns the ``url_hash`` - this differs slightly from the Anvil implementation.
    It does not convert a query string to a dictionary automatically.

.. function:: routing.get_url_pattern(url_hash=None)

    Returns the part of the ``url_hash`` without the query string.

.. function:: routing.get_url_dict(url_hash=None)

    Returns a dictionary based on the query string of the ``url_hash``.


.. function:: routing.load_error_form

    Loads the error form at the current ``url_hash``.


.. function:: routing.remove_from_cache(url_hash)

    Removes a ``url_hash`` from the ``routing`` module's cache.

.. function:: routing.add_to_cache(url_hash, form)

    Adds a form to the cache at a specific ``url_hash``. Whenever the user navigates to this URL the cached form will be used.
    (Caching generally happens without you thinking about it).

.. function:: routing.clear_cache()

    Clears all forms and url_hash's from the cache.

.. function:: routing.get_cache()

    Returns the cache object from the ``routing`` module.
    Adjusting the cache directly may have side effects.



.. function:: routing.go(x=0)

    Go forward/back x number of pages. Use negative values to go back.

.. function:: routing.go_back()

    Go back one page.

.. function:: routing.reload_page(hard=False)

    Reload the current route_form (if ``hard = True`` the page will refresh)


.. function:: routing.on_session_expired(reload_hash=True, allow_cancel=True)

    Override the default behaviour for a session expired.
    Anvil's default behaviour will reload the app at the home form.

.. function:: routing.set_warning_before_app_unload(True)

    Pop up the default browser dialogue when navigating away from the app.


.. attribute:: routing.logger

    Logging information is provided when debugging.
    Logging is turned off by default.

    To turn logging on do: ``routing.logger.debug = True``.


Notes and Examples
------------------

The following represents some notes and examples that might be helpful


Routing Debug Print Statements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To debug your routing behaviour use the routing logger.
Routing logs are turned off by default.

To use the routing logger, in your ``MainForm`` do:

.. code:: python

    from anvil_extras import routing

    routing.logger.debug = True

    @routing.main_router
    class MainForm(MainFormTemplate):
        ...


Page Titles
^^^^^^^^^^^

You can set each ``Route Form`` to have a ``title`` parameter, which will
change the browser tab title

If you do not provide a title then the page title will be the default
title provided by Anvil in your titles and logos

.. code:: python

    @routing.route('', title='Home | RoutingExample')
    class Home(HomeTemplate):
        ...

.. code:: python

    @routing.route('article', url_keys=['id'], title="Article-{id} | RoutingExample")
    class ArticleForm(ArticleFormTemplate):
        ...

.. code:: python

    @routing.route('article/{id}', title='Article | {id}')
    class ArticleForm(ArticleFormTemplate):
        ...


-  Think f-strings without the f
-  Anything in curly braces should be an item from ``url_keys`` or a dynamic variable in the ``url_pattern``.

You can also dynamically set the page title,
for example, to values loaded from the database.

.. code:: python

    from anvil.js.window import document

    @routing.route('article', url_keys=['id'])
    class ArticleForm(ArticleFormTemplate):
      def __init__(self, **properties):
        self.item = anvil.server.call('get_article', article_id=self.url_dict['id'])
        document.title = f"{self.item['title']} | RoutingExample'"

        self.init_components(**properties)



Full-Width Rows
^^^^^^^^^^^^^^^

You can set a ``Route Form`` to load as a ``full_width_row`` by setting
the ``full_width_row`` parameter to ``True``.

.. code:: python

    @routing.route('', title='Home', full_width_row=True)
    class Home(HomeTemplate):
        ...


Multiple Route Decorators
^^^^^^^^^^^^^^^^^^^^^^^^^

It is possible to define optional parameters by adding multiple
decorators, e.g. one with and one without the key. Here is an example
that allows using the ``home page`` with the default empty string and
with one optional ``search`` parameter:

.. code:: python

    @routing.route('')
    @routing.route('', url_keys=['search'])
    class Form1(Form1Template):
      def __init__(self, **properties):
        self.init_components(**properties)
        self.search_terms.text = self.url_dict.get('search', '')

Perhaps your form displays a different ``item`` depending on the
``url_pattern``/ ``url_hash``:

.. code:: python

    @routing.route('articles')
    @routing.route('blogposts')
    class ListItems(ListItemsTemplate):
      def __init__(self, **properties):
        self.init_components(**properties)
        self.item = anvil.server.call(f'get_{self.url_pattern}')
        # self.url_pattern is provided by the routing module


Form Arguments
^^^^^^^^^^^^^^

It's usually better to avoid required named arguments for a Form.
Something like this is not allowed:

.. code:: python

    @routing.route('form1', url_keys=['key1'])
    class Form1(Form1Template):
      def __init__(self, key1, **properties):
        ...

All the parameters listed in ``url_keys`` are required, and the rule is
enforced by the routing module. If the ``Route Form`` has required
``url_keys`` then the routing module will provide a ``url_dict`` with
the parameters from the ``url_hash``.

This is the correct way:

.. code:: python

    @routing.route('form1', url_keys=['key1'])
    class Form1(Form1Template):
      def __init__(self, **properties):
        key1 = self.url_dict['key1']
        #routing provides self.url_dict



Main Router Callbacks
^^^^^^^^^^^^^^^^^^^^^

There are two callbacks available for a ``MainForm``.

-  ``on_navigation``: called whenever the ``url_hash`` changes
-  ``on_form_load``: called after a form is loaded into the ``content_panel``


``on_navigation`` example:
~~~~~~~~~~~~~~~~~~~~~~~~~~

To use the Material Design role ``'selected'`` for sidebar links,
create an ``on_navigation`` method in your ``MainForm``.

.. code:: python

    @routing.main_router
    class MainForm(MainFormTemplate):
      def __init__(self, **properties):
        self.init_components(**properties)
        self.links = [self.articles_link, self.blog_posts_link]
        self.blog_posts_link.tag.url_hash = 'blog-posts'
        self.articles_link.tag.url_hash   = 'articles'

      def on_navigation(self, **nav_args):
        # this method is called whenever routing provides navigation behaviour
        # url_hash, url_pattern, url_dict are provided by the main_router class decorator
        for link in self.links:
          if link.tag.url_hash == nav_args.get('url_hash'):
            link.role = 'selected'
          else:
            link.role = 'default'


**Nav Args will look like:**

.. code:: python

    nav_args = {'url_hash':    url_hash,
                'url_pattern': url_pattern,
                'url_dict':    url_dict,
                'unload_form': form_that_will_be_unloaded # could be None if initial call
                }

``on_form_load`` example:
~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to use animation when a form is loaded you might use the
``on_form_load`` method.

.. code:: python

      def on_form_load(self, **nav_args):
          # this method is called whenever the routing module has loaded a form into the content_panel
          form = nav_args["form"]
          animate(form, fade_in, duration=300)


Note if you wanted to use a fade-out you could also use the
``on_navigation`` method.

.. code:: python

      def on_navigation(self, **nav_args):
          # this method is called whenever the url_hash changes
          form = nav_args["unload_form"]
          animate(form, fade_out, duration=300).wait()
          # wait for animation before continuing



Navigation Techniques
^^^^^^^^^^^^^^^^^^^^^

``redirect=False``
~~~~~~~~~~~~~~~~~~

It is possible to set a new URL without navigating away from the current
form. For example, a form could have this code:

.. code:: python

    def search_click(self, **event_args):
      if self.search_terms.text:
          routing.set_url_hash(f'?search={self.search_terms.text}',
                               redirect=False
                              )
      else:
          routing.set_url_hash('',
                               redirect=False,
                              )
      self.search(self.search_terms.text)

This way search parameters are added to the history stack so that the
user can navigate back and forward, but routing does not attempt to
navigate to a new form instance.

Important
~~~~~~~~~

Be careful if you use ``routing.set_url_hash`` inside the ``__init__`` method or
``form_show`` event. You may cause an infinite loop if your
``url_hash`` points to the same form and ``redirect=True``! In this
case, you will get a ``warning`` from the ``routing.logger`` and
navigation/redirection will be halted.

Navigation will be halted after 5 navigation attempts without
loading a form to the ``content_panel``.

``replace_current_url=True``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is also possible to replace the current URL in the history stack
rather than creating a new entry in the history stack.

In the demo app the ``ArticleForm`` creates a new article
if the ``id`` parameter is empty like: ``url_hash = "article?id="``

.. code:: python

    @routing.route('article', url_keys=['id'])
    class ArticleForm(ArticleFormTemplate):
        def __init__(self, **properties):
            self.init_components(**properties)
            if url_dict['id']:
                self.item = anvil.server.call("get_article_by_id", self.url_dict['id'])
            else:
                # url_dict['id'] is empty
                self.item = anvil.server.call('create_new_article')
                routing.set_url_hash(f"article?id={self.item['id']",
                                     replace_current_url=True,
                                     set_in_history=True,
                                     redirect=False
                                    )


See `API Docs <#api>`__ for a list of valid kwargs for ``routing.set_url_hash()``.


Changing The Main Form
^^^^^^^^^^^^^^^^^^^^^^

In a more complex app, it's common to want to change the Main Form.
At present, changing the Main Form is not supported (support may be added in a future release).

Instead, it is recommended to change the structure of the Main Form dynamically
(sidebar, navbar and title) based on the ``url_hash``.

Let's say you have an admin part of the app and a standard part of the app.
All admin content starts with ``admin/``.

Use the ``on_navigation`` callback to change the sidebar and title components.

.. code:: python

    def on_navigation(self, url_hash, **nav_args):
        is_admin = url_hash.startswith("admin/")
        if is_admin is not self.is_admin:
            self.setup(admin=is_admin)

    def setup(self, admin=False):
        if admin:
            self.sidebar = self.admin_sidebar_panel
            self.title_label.text = "Admin"
        else:
            self.sidebar = self.main_sidebar_panel
            self.title_label.text = "Main"
        self.clear(slot="left-nav")
        self.add_component(self.sidebar, slot="left-nav")
        self.is_admin = admin


An alternative might be to use the form_show event of various Route Forms.
We can outsource managing the Main Form structure changes to a separate module.
In this example, the module is called Manager and contains functions for changing sidebar
links and the title. This code depends on the main form having a column
panel called ``sidebar_panel`` for the sidebar links, and a label called
title for the title.

.. code:: python

    import anvil
    from anvil_extras import routing

    def _handle_click(sender, **event_args):
        routing.set_url_hash(sender.tag.url_hash)

    def _make_link(text, url):
        link = anvil.Link(text=text)
        link.tag.url_hash = url
        link.set_event_handler('click', _handle_click)
        return link

    _home_links = [{'text': 'About', 'url': 'about'}, {'text': 'News', 'url': 'news'}]
    _news_links = [{'text': 'Last Month', 'url': 'last-month'}, {'text': 'Home', 'url': ''}]

    _sidelinks = {
        'home': [_make_link(**link_def) for link_def in _home_links)],
        'news': [_make_link(**link_def) for link_def in _news_links)],
    }

    def setup_sidelinks(id):
        if id not in _sidelinks:
            return

        sidebar_panel = anvil.get_open_form().sidebar_panel

        if sidebar_panel.tag.current == id:
            return

        sidebar_panel.clear()
        sidebar_panel.tag.current = id

        for link in _sidelinks[id]:
            links_panel.add_component(sidelink)


    def set_title(title):
        anvil.get_open_form().title.text = title


Then, in every form that is a routing target,
you tell the manager which sidebar links and title to display.
Multiple forms can use the same set of sidebar links.

.. code:: python

    def form_show(self, **event_args):
        # We setup the side navigation links in form show, so that when the form is navigated
        # away from and back again we can set up the links again.
        Manager.setup_sidelinks('home')
        Manager.set_title('Home')


Security
^^^^^^^^

**Security issue**: You log in, open a form with some data, go to the
next form, log out, go back 3 steps and you see the cached stuff that
was there when you were logged in.

**Solution 1**: When a form shows sensitive data it should always check
for user permission in the ``form_show`` event, which is triggered when
a cached form is shown.

**Solution 2**: Call ``routing.clear_cache()`` to remove the cache upon
logging out.

--------------


Preventing a Form from Unloading (when navigating within the app)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a method in a ``Route Form`` called ``before_unload``

To prevent Unloading return a value

.. code:: python

    def before_unload(self):
      # this method is called when the form is about to be unloaded from the content_panel
      if confirm('are you sure you want to close this form?'):
        pass
      else:
        return 'STOP'

*NB*: - Only use if you need to prevent unloading. - Otherwise, the
``form_hide`` event should work just fine.

*NB*: - This method does not prevent a user from navigating away from
the app entirely. (see the section `Leaving the
App <#leaving-the-app>`__ below)

--------------

Passing properties to a form
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can pass properties to a form by adding them as keyword arguments to ``routing.set_url_hash``

.. code:: python

    def article_link_click(self, **event_args):
      routing.set_url_hash(f'article?id={self.item["id"]'}, item=self.item)

--------------

Sometimes my Route Form is a Route Form sometimes it is a Component
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

No problem... use the parameter ``route=False`` to avoid typical routing
behaviour

.. code:: python

    def button_click(self,**event_args):
      alert(ArticleForm(route=False))
      # setting route = False stops the Route Form using the routing module...

--------------

My ``url_dict`` contains the & symbol
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's say your ``url_dict`` is ``{'name': 'A&B'}`` doing the following
will cause a problem

.. code:: python

    routing.set_url_hash('customer?name=A&B')

instead, do

.. code:: python

    routing.set_url_hash(url_pattern='customer', url_dict={'name':'A&B'})

``anvil_extras.routing`` will encode this correctly

--------------

I have a login form how do I work that?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**As part of anvil_extras.routing**

.. code:: python

    @routing.main_router
    class MainForm(MainFormTemplate):
      def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        user = anvil.users.get_user()
        if user is None:
          routing.set_url_hash('login',
                               replace_current_url=True,
                               redirect=False
                               )
        # after the init method the main router will navigate to the login form so no need to redirect

Then for the ``LoginForm``

.. code:: python

    @routing.route('login')
    class LoginForm(LoginFormTemplate):
      def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.

      def form_show(self, **event_args):
        """This method is called when the column panel is shown on the screen"""
        user = anvil.users.get_user()
        while not user:
          user = anvil.users.login_with_form()

        routing.remove_from_cache(self.url_hash)  # prevents the login form loading from cache in the future...
        routing.set_url_hash('',
                             replace_current_url=True,
                             redirect=True
                             )
        # '' replaces 'login' in the history stack and redirects to the HomeForm

**Separate from anvil_extras.routing**

Rather than have the ``LoginForm`` be part of the navigation, you could
create a startup module that will call ``open_form("LoginForm")`` if no user is logged in.
The ``LoginForm`` should **not** have any ``anvil_extras.routing`` decorators.

Then when the user has signed in you can call ``open_form('MainForm')``.
The ``main_router`` will then take control of the ``url_hash`` based
navigation.

When the user signs out you can call ``open_form('LoginForm')`` and the
``main_router`` will no longer have control of the navigation. There
will still be entries when the user hits back/forward navigation (i.e.
the ``url_hash`` will change but there will be no change in forms...)
:smile:

(You will need to add an on\_navigation method to the ``LoginForm``,
which does nothing, to keep the ``routing`` module happy)

.. code:: python

    def on_navigation(self):
        pass

--------------

I have a page that is deleted - how do I remove it from the cache?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python


    def trash_link_click(self, **event_args):
      """called when trash_link is clicked removes the """
      self.item.delete()  # table row
      routing.remove_from_cache(self.url_hash) # self.url_hash provided by the @routing.route class decorator
      routing.set_url_hash('articles',
                            replace_current_url=True,
                          )

And in the ``__init__`` method - you will want something like:

.. code:: python

    @routing.route('article', keys=['id'], title='Article-{id}')
    class ArticleForm(ArticleFormTemplate):
      def __init__(self, **properties):
        try:
          self.item = anvil.server.call('get_article_by_id', self.url_dict['id'])
        except:
          routing.set_url_hash('articles', replace_current_url=True)
          raise Exception('This article does not exist or has been deleted')


--------------

Form Show is important
^^^^^^^^^^^^^^^^^^^^^^

since the forms are loaded from cache you may want to use the
``form_show`` events if there is a state change

Example 1
~~~~~~~~~

When that article was deleted in the above example we wouldn't want the
deleted article to show up on the ``repeating_panel``

so perhaps:

.. code:: python

    @routing.route('articles')
    class ListArticlesForm(ListArticlesFormTemplate):
      def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.repeating_panel.items = anvil.server.call('get_articles')

        # Any code you write here will run when the form opens.

      def form_show(self, **event_args):
        """This method is called when the column panel is shown on the screen"""
        self.repeating_panel.items = anvil.server.call_s('get_articles')
        # silent call to the server on form show

**An alternative approach to the above scenario:**

set ``load_from_cache=False``

That way you wouldn't need to utilise the show event of the
``ListArticlesForm``

.. code:: python

    @routing.route('article', keys=['id'], title='Article-{id}')
    class ArticleForm(ArticleFormTemplate):
      def __init__(self, **properties):
        try:
          self.item = anvil.server.call('get_article_by_id', self.url_dict['id'])
        except:
          routing.set_url_hash('articles', replace_current_url=True, load_from_cache=False)

      def trash_link_click(self, **event_args):
        """called when trash_link is clicked removes the """
        self.item.delete()  # table row
        routing.remove_from_cache(self.url_hash) # self.url_hash provided by the @routing.route class decorator
        routing.set_url_hash('articles',
                             replace_current_url=True,
                             load_from_cache=False)


Example 2
~~~~~~~~~

In the search example above the same form represents multiple
``url_hash``\ s in the cache.

No problem.

Whenever navigation is triggered by clicking the back/forward buttons, the
``self.url_hash``, ``self.url_dict`` and ``self.url_pattern`` are
updated and the ``form_show`` event is triggered.

.. code:: python

    def form_show(self, **event_args):
      search_text = self.url_dict.get('search','')
      self.search_terms.text = search_text
      self.search(search_text)

--------------

Leaving the app
^^^^^^^^^^^^^^^

Routing implements `W3 Schools
onbeforeunload <https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_onbeforeunload_dom>`__
method.

This warns the user before navigating away from the app using a default
browser warning. (This may not work on ios)

By default, this setting is switched off. To switch it on do:
``routing.set_warning_before_app_unload(True)``

To implement this behaviour for all pages change the setting in your
``MainForm`` like:

.. code:: python

    from anvil_extras import routing

    routing.set_warning_before_app_unload(True)

    @routing.main_router
    class MainForm(MainFormTemplate):

To implement this behaviour only on specific ``Route Forms`` toggle the
setting like:

.. code:: python

    def form_show(self, **event_args):
      routing.set_warning_before_app_unload(True)

    def form_hide(self, **event_args):
      routing.set_warning_before_app_unload(False)

Or based on a parameter (See the example app ``ArticleForm`` code for a
working example)

.. code:: python

    def edit_status_toggle(status):
      routing.set_warning_before_app_unload(status)

*NB:* When used on a specific ``Route Form`` this should be used in
conjunction with the ``before_unload`` method (see above).
