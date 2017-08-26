## Item Catalog Project

This repository includes Udacity project unit 3

A user of this project can add, edit, and delete items belonging to a particular category.

Authentication is handled by Facebook OAuth. User can only edit or delete items they have created

## Prerequisites

Requires Python, pip, and git.

## How to Install

To download and install this program, you will need git installed.

At the command line, enter:

git clone https://github.com/alanriddle/fs_proj3_item_catalog.git
Change directory to fs_proj3_item_catalog.

## How to Use Facebook Oauth Login
please visit: https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow





## How to Initialize Database and Load Initial Categories

To initialize the SQLite database (create empty tables) enter

python db/database_setup.py
To load the initial sporting good categories enter

python db/lots_of_menus.py
populate DB with initial dummies

## Starting Application

To start the application enter:

python project.py
Then bring up a browser and point it to localhost:8000.

## Adding, Editing, and Deleting Items

Adding, editing, and deleting items requires the user to log in. Logins are handled by Facebook OAuth.
remember to setup http://localhost:8000/ in your application inside FB dev tool if you want to Test locally

Users can see all items but can only edit and delete their own items. This has been tested with two users.
