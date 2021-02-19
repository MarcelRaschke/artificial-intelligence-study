import os
import logging
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify, render_template
from PIL import Image
import io
import traceback

from ocr import process_image, process_image2

app = Flask(__name__)
_VERSION = 1  # API version


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/v{}/ocr'.format(_VERSION), methods=["POST"])
def ocr():
    print('--call ocr processing --')
    try:
        if request.files.get("image"):
            print('--read image --')
            # read the image in PIL format
            image = request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            print('RECV:', image.format, image.size, image.mode)

            output = process_image2(image)
            print('output:', output)
            return jsonify({"output": output})
        else:
            return jsonify({"error": "only .jpg files, please"})
    except Exception as e:
        print('ocr processing exception:' , e)
        print(traceback.format_exc())
        return jsonify(
            {"error": str(e)}
        )


#@app.errorhandler(500)
#def internal_error(error):
#    print str(error)  # ghetto logging

#@app.errorhandler(404)
#def not_found_error(error):
#    print str(error)

#if not app.debug:
#    file_handler = FileHandler('error.log')
#    file_handler.setFormatter(
#        Formatter('%(asctime)s %(levelname)s: \
#            %(message)s [in %(pathname)s:%(lineno)d]')
#    )
#    app.logger.setLevel(logging.INFO)
#    file_handler.setLevel(logging.INFO)
#    app.logger.addHandler(file_handler)
#    app.logger.info('errors')


if __name__ == '__main__':
    #app.debug = True
    #port = int(os.environ.get('PORT', 5000))
    #app.run(host='127.0.0.1', port=port)
    app.run(debug=True, host='0.0.0.0', port=5000, threaded = True)
    print("--end--")
