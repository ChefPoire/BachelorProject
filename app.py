# Imports
import os
from flask import Flask, render_template, request, send_file, redirect, url_for, send_from_directory, flash, send_from_directory
from processing.VSItoPNG import vsi_to_png
from processing import slice_processing
from PIL import Image
import numpy as np
import plotly.graph_objects as go
import pyvista as pv

# Config
# Folder where uploaded .vsi files are stored
UPLOAD_FOLDER = "static/uploads"
# Folder where generated .png files are stored
OUTPUT_FOLDER = "static/outputs"
# List of allowed extensions for uploaded files
ALLOWED_EXTENSIONS = {"vsi", "ply"}

# Initialize Flask webapp
app = Flask(__name__)
app.secret_key = "supersecretkey" # needed for flash messages

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

# Create folders if they don't  exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Homepage with welcome message
    """
    if request.method == "POST":
        return render_template("upload.html")
    else:
        return render_template("index.html")

@app.route("/upload", methods=["GET","POST"])
def upload_file():
    """
    Handle file upload and conversion.
    """
    # When a file is uploaded (POST-route)
    if request.method == "POST":

        # If no file is found, redirect to new request
        if "file" not in request.files:
            flash("No file part in request")
            return render_template("upload.html")

        # If no file is selected, redirect to new request
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return render_template("upload.html")
        
        # If a file is selected, and has an allowed extension
        if file and allowed_file(file.filename.lower()):
            vsi_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(vsi_path)
            
            # Uploaded file is .vsi (Brain Slices)
            if file.filename.lower().endswith(".vsi"):
                # Convert to VSI to PNG using converter
                try:
                    vsi_to_png(vsi_path, app.config["OUTPUT_FOLDER"], level=0)
                except Exception as e:
                    flash(f"Error converting VSI file: {e}")
                    return render_template("upload.html")
                        
                # Get the output file  name
                base_name = os.path.splitext(file.filename)[0]
                png_filename = f"{base_name}_L0.png"
                return render_template("result.html", image_file = png_filename)
        
            # Uploaded file is .ply (3D Brain Scan)
            elif file.filename.lower().endswith(".ply"):

                # Convert to ASCII
                mesh = pv.read(vsi_path)

                ascii_name = os.path.splitext(file.filename)[0] + "_ascii.ply"
                ascii_path = os.path.join(app.config["UPLOAD_FOLDER"], ascii_name)

                mesh.save(ascii_path, binary=False)

                return redirect(url_for("view_3d", filename=ascii_name))
    
    # When you land on this page the first time
    elif request.method == "GET":
        flash("Please upload a valid .vsi file.")
        return redirect(url_for("index"))

@app.route("/view_3d/<filename>")
def view_3d(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if not os.path.exists(file_path):
        flash("File not found.")
        return redirect(url_for("index"))
    return render_template("view_3d.html", ply_file=filename)

@app.route("/static/images/<filename>")
def uploaded_file(filename):
    """
    Serve generated PNG images.
    """
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename)

@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)



if __name__ == "__main__":
    app.run(debug=True)
