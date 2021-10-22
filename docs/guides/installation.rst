Installation
============
There are two options for installling anvil-extras:

#. As a third-party dependency

   This is the simplest option. After you add the library to your app, there is no
   further maintenance involved and updates will happen automatically.
#. As a clone

   This option involves using git on your local machine to manage your own copy of the
   anvil-extras library. There is more work involved but you gain full control over when
   and if your copy is updated.

NOTE: If you are an enterprise user, you cannot use the third-party dependency option.

Install as a third-party dependency
-----------------------------------
* From the gear icon at the top of your app's left hand sidebar, select 'Dependencies'
* In the buttons to the right of 'Add a dependency', click the 'Third Party' button
* Enter the id of the Anvil-Extras app: C6ZZPAPN4YYF5NVJ
* Hit enter and ensure that the library appears in your list of dependencies
* Select whether you wish to use the 'Development' or 'Published' version

For the published version, the dependency will be automatically updated as new versions are released.
On the development version, the update will occur whenever we merge new changes into the library's code base.

Whilst we wouldn't intentionally merge broken code into the development version, you should
consider it unstable and not suitable for production use.

Install as a clone
------------------

Clone the Repository
++++++++++++++++++++
* In your browser, navigate to your blank Anvil Extras app within your Anvil IDE.
* From the App Menu (with the gear icon), select 'Version History...' and click the 'Clone with Git' button.
* Copy the displayed command to you clipboard.
* In your terminal, navigate to a folder where you would like to create your local copy
* Paste the command from your clipboard into your terminal and run it.
* You should now have a new folder named 'Anvil_Extras'.

Configure the Remote Repositories
+++++++++++++++++++++++++++++++++
Your local repository is now configured with a known remote repository pointing to your copy of the app at Anvil.
That remote is currently named 'origin'. We will now rename it to something more meaningful and also add a second remote pointing to the repository on github.

* In your terminal, navigate to your 'Anvil_Extras' folder.
* Rename the 'origin' remote to 'anvil' with the command:

.. code-block::

    git remote rename origin anvil

* Add the github repository with the command:

.. code-block::

    git remote add github git@github.com:anvilistas/anvil-extras.git

Update your local app
+++++++++++++++++++++
To update your app, we will now fetch the latest version from github to your local copy and push it from there to Anvil.

* In your terminal, fetch the lastest code from github using the commands:

.. code-block::

    git fetch github
    git reset --hard github/main

* Finally, push those changes to your copy of the app at Anvil:

.. code-block::

    git push -f anvil


Add anvil-extras as a dependency to your own app(s)
+++++++++++++++++++++++++++++++++++++++++++++++++++
* From the gear icon at the top of your app's left hand sidebar, select 'Dependencies'
* From the 'Add a dependency' dropdown, select 'Anvil Extras'

That's it! You should now see the extra components available in your app's toolbox on the right hand side and all the other features are available for you to import.
