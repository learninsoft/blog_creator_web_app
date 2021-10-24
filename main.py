from website import create_site
from flask import request
app = create_site()

if __name__ == "__main__":
    app.run(debug=True, port=8000)

# export FLASK_APP=main.py
# FLASK_APP=main:app
# python -m flask db init
# python -m flask db migrate
# python -m flask db upgrade
