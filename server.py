from flask_app import app

# from flask_app.controllers import users


# error handler
@app.errorhandler(404)
def not_found(e):
    return "Sorry! No response. Try again."


if __name__ == "__main__":
    app.run(debug=True)
