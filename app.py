# Imports
import os
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from processing.VSItoPNG import convert_vsi_to_png

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
ALLOWED_EXTENSIONS = {"vsi"}

app = Flask(__name__)
app.secret_key = "supersecretkey" # needed for flash messages
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET","POST"])
def upload_file():
    """
    Upload a file to the website for 3D modelling.
    """
    # When a file is uploaded
    if request.method == "POST":

        # If no file is found, redirect to new request
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]

        # If no file is selected, redirect to new request
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        
        # If a file is selected, and has an allowed extension
        if file and allowed_file(file.filename):
            vsi_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(vsi_path)

            # Convert to PNG
            output_path = convert_vsi_to_png(vsi_path, app.config["OUTPUT_FOLDER"], user_series_number=1)

            flash(f"File converted succesfully: {os.path.basename(output_path)}")
            return send_file(output_path, as_attachment=True)
        
    return render_template("upload.html")
   

if __name__ == "__main__":
    app.run(debug=True)
