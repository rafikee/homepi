import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from os import walk

app = Flask(__name__)

# show the form to submit the upload
@app.route("/upload/<athan>", methods=["GET", "POST"])
def choose_file(athan):
    confirmation = ""
    if request.method == "POST":
        if athan == "delete_forever":
            file_path = request.form["file_path"]
            athan = "deleted"
            file_name = file_path.split("/")[1]
            os.remove(f"static/{file_path}")
            confirmation = "permanently removed " + file_path
        elif athan == "restore":
            file_path = request.form["file_path"]
            athan = file_path.split("/")[1]
            file_name = file_path.split("/")[1] + "/" + file_path.split("/")[2]
            os.rename(f"static/{file_path}", f"static/{file_name}")
            confirmation = "restored " + file_name
        elif athan == "delete":
            file_path = request.form["file_path"]
            athan = "deleted"
            os.rename(f"static/{file_path}", f"static/deleted/{file_path}")
            confirmation = "deleted " + file_path
        else:
            f = request.files["file"]
            filename = secure_filename(f.filename)
            f.save(os.path.join("static/" + athan, filename))
            confirmation = "Successfully uploaded " + filename

    # Display the files in the folder
    if athan != "deleted":
        filenames = next(walk("static/" + athan), (None, None, []))[2]  # [] if no file
        filenames = [x for x in filenames if ".git" not in x]  # drop the hidden files
        # don't let them change play.mp3
        filenames = [x for x in filenames if x != "play.mp3"]
        audio_files = [athan + "/" + x for x in filenames]
    else:
        audio_files = []
        for folder in next(walk("static/deleted"))[1]:
            filenames = next(walk("static/" + athan + "/" + folder), (None, None, []))[
                2
            ]  # [] if no file
            filenames = [
                x for x in filenames if ".git" not in x
            ]  # drop the hidden files
            audio_files.extend([athan + "/" + folder + "/" + x for x in filenames])
    return render_template(
        "upload.html", audio_files=audio_files, athan=athan, confirmation=confirmation
    )


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")
