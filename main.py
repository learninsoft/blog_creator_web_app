from website import create_site


if __name__ == "__main__":
    app = create_site()
    app.run(debug=True, port=8000)
