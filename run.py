from website import create_app, create_db

# Run the app

if __name__ == '__main__':
    app = create_app()
    create_db(app)
    app.run(debug=True, host='0.0.0.0', port=5000)