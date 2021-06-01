set -e  # Configure shell so that if one command fails, it exits
coverage erase
coverage run manage.py test --settings=personal_portfolio.settings_local
coverage report