from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return ("Hello World!\n"
            "How in the world am I gonna build frontend with it?!")


if __name__ == "__main__":
    app.run()
