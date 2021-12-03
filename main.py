from website import create_site

app = create_site()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

# export FLASK_APP=main.py
# FLASK_APP=main:app
# python -m flask db init
# python -m flask db migrate
# python -m flask db upgrade
