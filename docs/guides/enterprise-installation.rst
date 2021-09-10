Installation on Anvil Enterprise
============

Enterprise installations of Anvil are entirely separate from the cloud version by design, so you won't be able to depend on the public version of anvil-extras directly.
Instead, create an app on your Enterprise installation called Anvil Extras, then:


Clone the Repository
--------------------
* In your browser, navigate to your blank Anvil Extras app within your Anvil IDE.
* From the App Menu (with the gear icon), select 'Version History...' and click the 'Clone with Git' button.
* Copy the displayed command to you clipboard.
* In your terminal, navigate to a folder where you would like to create your local copy
* Paste the command from your clipboard into your terminal and run it.
* You should now have a new folder named 'Anvil_Extras'.

Configure the Remote Repositories
---------------------------------
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
--------------
To update your app, we will now fetch the latest version from github to your local copy and push it from there to Anvil.

* In your terminal, fetch the lastest code from github using the commands:

.. code-block::

    git fetch github
    git reset --hard github/main

* Finally, push those changes to your copy of the app at Anvil:

.. code-block::

    git push -f anvil



Add anvil-extras as a dependency to your own app(s)
---------------------------------------------------

* From the gear icon at the top of your app's left hand sidebar, select 'Dependencies'
* From the 'Add a dependency' dropdown, select 'Anvil Extras'

That's it! You should now see the extra components available in your app's toolbox on the right hand side and all the other features are available for you to import.
