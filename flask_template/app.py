#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
import conv_to_csv
import predict_dial_tags
import make_datafiles
import run_summarization
# from pointer_generator import 
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
my_dir = ""


### Load your model over here ###

# model = lambda x: x

def predict(input):
    input = "speaker:pos\n" + input
    with open(my_dir + '0.csv','w') as file:
        for line in input:
            file.write(line)
        file.write('\n')
    conv_to_csv.run()
    predict_dial_tags.run()
    make_datafiles.run()
    run_summarization.run(len(input.split()))
    with open(my_dir + "pretrained_model/output/decoded/000000_decoded.txt",'r') as file:
        output = file.readlines()
    output = " ".join(output)
    return output

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        ## Called after submit button is clicked
        output = predict(request.form['input_text'])
        template = render_template('index.html', result=output)
        return template

    if request.method == 'GET':
        return render_template('index.html')


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
