============
Dota2 badges
============

``san`` is a project built on Sanic and Opendota API, using Redis as data cache.

Install
=======

It's strongly suggested to use ``pipenv`` to install and manage the Python dependencies!

    pipenv install && pipenv shell

And also, you need to have Redis installed and started, assuming it's running at ``redis://localhost:6379``.

Running
=======

Now you can run ``python app.py`` and open link like ``http://localhost:8000/[your_steam_id]/mmr.svg`` to get your MMR badge:

.. image:: https://cdn.rawgit.com/kxxoling/san/master/mmr.svg
