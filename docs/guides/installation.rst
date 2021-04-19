Installation
============
Anvil-Extras is intended to be used as a dependency for other Anvil applications.

1. Clone anvil-extras to your account:

   .. image:: https://anvil.works/img/forum/copy-app.png
      :height: 40px
      :target: https://anvil.works/build#clone:C6ZZPAPN4YYF5NVJ=UGGCKFPRVZ7ELJH6RRZTHV6Y

2. Add anvil-extras as a dependency to your own app(s):

   * From the gear icon at the top of your app's left hand sidebar, select 'Dependencies'
   * From the 'Add a dependency' dropdown, select 'Anvil-Extras'

That's it! You should now see the extra components available in your app's toolbox on the right hand side and all the other features are available for you to import.

Upgrading
=========
To upgrade to a new release of Anvil-Extras, you will need to create a local copy of this repository and use git to update your copy of the app.

Clone the Repository
--------------------
* In your browser, navigate to your installed copy of the app within the Anvil IDE.
* From the App Menu (with the gear icon), select 'Version History...' and click the 'Clone with Git' button.
* Copy the displayed command to you clipboard.
* In your terminal, navigate to a folder where you would like to create your local copy
* Paste the command from your clipboard into your terminal and run it.
* You should now have a new folder named 'anvil_extras'.

Configure the Remote Repositories
---------------------------------
Your local repository is now configured with a known remote repository pointing to your copy of the app at Anvil.
That remote is currently named 'origin'. We will now rename it to something more meaningful and also add a second remote pointing to the repository on github.

* In your terminal, navigate to your 'anvil_extras' folder.
* Rename the 'origin' remote to 'anvil' with the command:

```
git remote rename origin anvil
```

* Add the github repository with the command:

```
git remote add github git@github.com:anvilistas/anvil-extras.git
```

Do the Upgrade
--------------
To upgrade your app, we will now fetch the latest version from github to your local copy and push it from there to Anvil.

* In your terminal, fetch the lastest code from github using the commands:

```
git fetch github
git reset --hard github/main
```

* Finally, push those changes to your copy of the app at Anvil:

```
git push -f anvil
```
