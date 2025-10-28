# Imports
import os
from flask import Flask, render_template, request, send_file, redirect, url_for, send_from_directory, flash
from processing.VSItoPNG import vsi_to_png
from processing import slice_processing
from PIL import Image
import numpy as np
import plotly.graph_objects as go

# Config
# Folder where uploaded .vsi files are stored
UPLOAD_FOLDER = "static/uploads"
# Folder where generated .png files are stored
OUTPUT_FOLDER = "static/outputs"
# List of allowed extensions for uploaded files
ALLOWED_EXTENSIONS = {"vsi"}

# Initialize Flask webapp
app = Flask(__name__)
app.secret_key = "supersecretkey" # needed for flash messages

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

# Create folders if they don't  exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS # <-- hier zit mogelijk een foutje in...

# # # # #
# Webapp logic: app routes
# Foutje in de index en upload routes...`
# # # # # 


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
            print("#### 1 >>>> TOT HIER KOMT IE!!!")
            # Convert to VSI to PNG using converter
            try:
                print("#### 2 >>>> TOT HIER KOMT IE!!!")
                vsi_to_png(vsi_path, app.config["OUTPUT_FOLDER"], level=0)
                print("#### 3 >>>> TOT HIER KOMT IE!!!")
            except Exception as e:
                flash(f"Error converting VSI file: {e}")
                return render_template("upload.html")
            
            # Get the output file  name
            base_name = os.path.splitext(file.filename)[0]
            png_filename = f"{base_name}_L0.png"

            return render_template("result.html", image_file = png_filename)
        
    elif request.method == "GET":
        flash("Please upload a valid .vsi file.")
        return redirect(url_for("index"))

@app.route("/static/images/<filename>")
def uploaded_file(filename):
    """
    Serve generated PNG images.
    """
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename)

@app.route("/slice-preparer", methods=["GET","POST"])
def slice_preparer():
    """
    Web interface for 2D slice preparation.
    Allows upload, cut, remove background, store slice, and send slices to 3D viwer.
    """
    upload_file_url = None
    processed_file_url = None
    stored_slice_urls = [f"/{OUTPUT_FOLDER}/{i}.png" for i in range(len(slice_processing.get_stored_slices()))]

    if request.method == "POST":
        action = request.form.get("action")

        # --- Handle image upload ---
        if action == "upload":
            file = request.files["file"]
            if file:
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)
                uploaded_file_url = f"/{filepath}"
                return redirect(url_for("slice_preparer"))
        
        # --- Get uploaded image ---
        filename = request.form.get("filename")
        if not filename:
            filename = os.listdir(UPLOAD_FOLDER)[-1] # take last uploaded
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        img = Image.open(filepath)

        # --- Cut slice ---
        if action == "cut":
            w, h = img.size
            box = (w//4, h//4, 3*w//4, 3*h//4) # example crop
            cropped = slice_processing.cut_slice(img, box)
            output_path = os.path.join(OUTPUT_FOLDER, "cropped.png")
            cropped.save(output_path)
            processed_file_url = f"/{output_path}"

        # --- Remove background ---
        elif action == "remove_bg":
            bg_color = (255,255,255) # default: white
            processed = slice_processing.remove_background(img, bg_color=bg_color)
            output_path = os.path.join(OUTPUT_FOLDER, "processed.png")
            processed.save(output_path)
            processed_file_url = f"/{output_path}"

        # --- Store slice ---
        elif action == "store_slice":
            slice_processing.store_slice(img)

            # save stored slice for preview
            stored_slice_urls = []
            for i, s in enumerate(slice_processing.get_stored_slices()):
                path = os.path.join(OUTPUT_FOLDER, f"{i}.png")
                s.save(path)
                stored_slice_urls.append(f"/{path}")

        # --- Clear stored slices ---
        elif action == "clear_slices":
            slice_processing.clear_stored_slices()
            stored_slice_urls = []

    # Update stored slice preview URLs
    stored_slice_urls = [f"/{OUTPUT_FOLDER}/{i}.png" for i in range(len(slice_processing.get_stored_slices()))]

    return render_template(
        "slice_preparer.html",
        uploaded_file_url = uploaded_file_url,
        processed_file_url = processed_file_url,
        stored_slice_urls = stored_slice_urls
    )

@app.route("/view-3d")
def view_3d():
    """
    Render stored slices as a 3D volume using Plotly.
    """
    slices = slice_processing.get_stored_slices()
    if not slices:
        return "<h3>No slices stored. Go back and store slices first.</h3>"

    # Converrt all stored slices to grayscale numpy arrays
    stack = []
    for img in slices:
        img_gray = img.convert("L")
        stack.append(np.array(img_gray))
    volume = np.stack(stack, axis=0)

    # Normalize to 0-1 for Plotly
    volume = volume / 255.0

    fig = go.Figure(data=go.Volume(
        x=np.repeat(np.arrange(volume.shape[2]), volume.shape[1]*volume.shape[0]),
        y=np.tile(np.repeat(np.arange(volume.shape[1]), volume.shape[0]), volume.shape[2]),
        z=np.tile(np.arrange(volume.shape[0]), volume.shape[1]*volume.shape[2]),
        value=volume.flatten(),
        colorscale="Gray"
    ))

    # Export Plotly figure als HTML div
    plot_div = fig.to_html(full_html=False)

    return render_template("view_3d.html", plot_div=plot_div)

if __name__ == "__main__":
    app.run(debug=True)
