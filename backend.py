from flask import Flask, render_template, jsonify
import stem.control

app = Flask(__name__)

TOR_CONTROL_PORT = 9051
TOR_PASSWORD = 'your_password'  # Set in torrc with 'HashedControlPassword'

def get_tor_status():
    try:
        with stem.control.Controller.from_port(port=TOR_CONTROL_PORT) as controller:
            controller.authenticate(password=TOR_PASSWORD)
            info = {
                "nickname": controller.get_info("nickname"),
                "version": controller.get_info("version"),
                "uptime": controller.get_info("uptime"),
                "bandwidth": controller.get_info("traffic/read") + " / " + controller.get_info("traffic/written"),
            }
            return info
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify(get_tor_status())

if __name__ == "__main__":
    app.run(debug=True)
