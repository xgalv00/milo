Install notes
===================

- git clone git@github.com:xgalv00/milo.git
- virtualenv -p python3 env
- source env/bin/activate
- cd milo
- pip install -r requirements/requirements.txt
- python manage.py migrate
- python manage.py runserver

Release notes
===================
Done
-------------------
- Set up a basic (latest or LTS) Django installation
- Extend the User model
- Create basic views
- Create template tags
- Unit testing
- Create a download link on the list view in [CSV]( https://prnt.sc/fn8iao )
- Add command to extract date from file (python task). Command code is located in users app

TODO (don't know if should be done)
-------------------
- Move secret key to .env or similar
- Deploy
- Admin interface not finished
- Better styling
- AJAX loading for user management

Screenshots
-------------------
* [No users]( https://prnt.sc/fn8iao )
* [Create user]( https://prnt.sc/fn8ih5 )
* [User details]( https://prnt.sc/fn8irc )
* [User list]( https://prnt.sc/fn8j6f )
* [Update user]( https://prnt.sc/fn8j04 )
* [Delete user]( https://prnt.sc/fn8jbk )
* [No users]( https://prnt.sc/fn8iao )
