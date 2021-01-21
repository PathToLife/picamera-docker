#!/usr/bin/env python
from flask import Flask, render_template, Response, request, send_file
from functools import wraps
import time
import config

# Robot Video Streaming Example with the Raspberry Pi Camera
# This example will show you how to stream video from your robot.  In this example we use
# Python, the Raspberry Pi Camera, and a Flask server on the GoPiGo.

# To Start:
# In the command line, type "sudo python stream_pi_camera.py"
# You can include the "&" symbol at the end to run in the background.

from camera import Camera

app = Flask(__name__)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == config.user and password == config.password


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route('/')
@requires_auth
def index():
    # Video streaming home page.
    # This should serve up your Raspberry Pi Camera video.
    return render_template('pi_camera_index.html')


def gen(camera):
    # Video streaming generator function.
    # For more on generator functions see Miguel Gringberg's beautiful post here:
    # https://blog.miguelgrinberg.com/post/video-streaming-with-flask
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/image')
@requires_auth
def get_image():
    buffer = Camera().get_image()
    filename = time.strftime("%Y%m%d-%H%M%S") + '.jpg'
    return send_file(
        buffer,
        as_attachment=True,
        attachment_filename=filename,
        mimetype='text/jpeg'
    )


@app.route('/video_feed')
@requires_auth
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag.
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
