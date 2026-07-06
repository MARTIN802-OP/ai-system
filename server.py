
from tool_server import create_file, run_command, read_file

app = Flask(__name__)

@app.route("/create-file", methods=["POST"])
def api_create_file():

    data = request.json

    result = create_file(
        data["path"],
        data["content"]
    )

    return jsonify(result)


@app.route("/run", methods=["POST"])
def api_run():

    data = request.json

    result = run_command(
        data["command"],
        data["cwd"]
    )

    return jsonify(result)


@app.route("/read-file", methods=["POST"])
def api_read():

    data = request.json

    content = read_file(data["path"])

    return jsonify({
        "content": content
    })


if __name__ == "__main__":

    app.run(port=5000)
