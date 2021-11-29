import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from os import walk

app = Flask(__name__)

# show the form to submit the upload
@app.route('/upload/<athan>', methods = ['GET', 'POST'])
def choose_file(athan, file_path = ""):
   confirmation = ""
   if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      f.save(os.path.join('static/' + athan, filename))
      confirmation = "Successfully uploaded " + filename
   if athan == 'delete':
      athan = 'deleted'
      file_name = file_path.split('/')[1]
      os.rename(f'static/{file_path}', f"static/deleted/{file_name}")

   filenames = next(walk('static/' + athan), (None, None, []))[2]  # [] if no file
   audio_files = [athan +'/' + x for x in filenames]
   return render_template('upload.html', audio_files=audio_files, athan=athan, confirmation=confirmation)
		
if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')