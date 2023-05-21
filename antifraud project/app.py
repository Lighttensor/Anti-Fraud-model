import os
from flask import Flask, render_template, request, redirect, url_for, send_file, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import src.processing


model_Xg, bagging = src.processing.load_models()
models = {"model_Xg": model_Xg,
          "bagging": bagging}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

class FileUploadForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Upload')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FileUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = file.filename
        session["filename"] = filename
        file.save(os.path.join('input', filename))
        src.processing.process_fraud(filename, models)
        return redirect(url_for('results'))
    return render_template('index.html', form=form)

# @app.route('/processing')
# def processing():
#     src.processing.process_fraud(filename, models)
#     return render_template('processing.html')

@app.route('/results')
def results():
    filename = request.args.get('filename')
    return render_template('results.html', filename=filename)

@app.route('/download')
def download():
    filename = session.get('filename')
    return send_file(os.path.join('output', filename), as_attachment=True)

# def process_file(filename):
#     app.logger.info(f'Processing file: {filename}')
#     if src.processing.process_fraud(filename, models)
#     app.logger.info(f'Finished processing file: {filename}')

if __name__ == '__main__':
    app.run(debug=True)

