# flask server for processing px4 log files and returning them on webserver
# TODO: change filename to reflect process
from flask import Flask
from flask import request
from flask import send_file
from sdlog2_dump import SDLog2Parser
import StringIO


app = Flask("log muncher")


@app.route("/", methods=["GET"])
def root():
    ret = ""
    ret += "<DOCTYPE html>"
    ret += "<form enctype=\"multipart/form-data\" method=\"post\">"
    ret += "<input type=\"file\" name=the_file>"
    ret += "<input type=\"submit\" value=Upload>"
    ret += "</form>"
    return ret


@app.route("/", methods=["POST"])
def process_log():
    f = request.files["the_file"]
    # parse
    log_filename = "log_temp"
    parser = SDLog2Parser()
    parser.setFileName(log_filename)
    parser.setCSVDelimiter(",")
    parser.setCSVNull("")
    parser.setMsgFilter([])
    parser.setTimeMsg("TIME")
    parser.setDebugOut(False)
    parser.setCorrectErrors(False)
    text = parser.process(f)
    # open file and return to user
    csv_text = ""
    with open(log_filename, "r") as f:
        csv_text = f.read()
    sio = StringIO.StringIO()
    sio.write(csv_text)
    sio.seek(0)
    return send_file(sio, attachment_filename="yo_file_dawg", as_attachment=True)


app.run("0.0.0.0", port=80, debug=True)
