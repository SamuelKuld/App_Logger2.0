from flask import Flask
import pickle
app = Flask("__name__")


@app.route("/")
def test():
    return "Test"


if __name__ == "__main__":
    app.run()
