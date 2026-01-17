# Bachelor Project Psychobiology: <br>3D Brain Imaging Project

## Description
This project is a web-based 3D visualization tool designed to support the exploration of neuroanatomical brain data. It enables users to upload, process, and visualize three-dimensional brain models derived from physical specimens. The tool was developed to improve accessibility, usability, and sustainability of neuroanatomical resources, particularly in educational and research contexts.

The application builds upon earlier prototype work by transforming a local, single-user visualization tool into an open-source web application. By relying exclusively on existing data and specimens from naturally deceased animals, the project aligns with ethical principles of animal well-being while expanding the possibilities for digital neuroanatomy.

### What does it do?
The 3D visualization tool allows users to:

- Upload 3D brain models (e.g. .ply-files) and microscopy data (e.g. .vsi-files) through a web interface
- Convert uploaded microscopy data into viewable image formats (not fully implemented yet)
- Visualize three-dimensional brain models directly in a browser environment
- Reuse previously generated models, reducing the need for new data acquisition

The tool is designed to support both educational use, such as teaching spatial neuroanatomy, and research-oriented exploration, including comparison of individual brain models.

### How does it work?
- Users access the application through a web browser and upload supported files via a simple interface.

- Uploaded files are handled by a Flask-based backend that validates, stores, and processes the data on the server.

    - Depending on the file type, the system routes the data through different processing pipelines:

    - Microscopy files are converted into image outputs (not fully implemented yet).

- 3D mesh files are prepared for interactive visualization.

- Processed outputs are made available to the user through the web interface, allowing inspection of images or 3D models without requiring specialized local software.

- The modular design allows future extensions, such as integrating tracer slice data into 3D models or expanding visualization functionality.

### Target Audience
The 3D brain visualization tool is primarily intended for students, educators, and researchers working with neuroanatomical data, and three-dimensional brain models in particular. These user groups were explicitly considered during the design and development of the application, with an emphasis on accessibility, clarity, and ease of use in both educational and research settings.

At the same time, the tool is not limited to these audiences. Any individual with access to suitable brain imaging or 3D anatomical data, and an interest in exploring or visualizing such data, can make use of the application. Its open-source nature and web-based implementation allow it to be adapted to a wide range of use cases beyond formal academic environments.

### Why a 3D visualization tool?
Understanding neuroanatomy requires insight into the three-dimensional spatial organization of brain structures and their connections. Traditional two-dimensional representations, such as histological slices or static atlas images, often fail to convey the complex geometry and spatial relationships that underlie brain function. While existing digital atlases provide valuable reference material, they typically focus on standardized brains and lack information about individual variability and anatomical connectivity derived from tracer experiments.

A 3D visualization tool addresses these limitations by enabling users to explore brain structures interactively in three dimensions. This allows for a more intuitive understanding of anatomical relationships, and supports the visualization of individual brains rather than population averages. By making these models accessible through a web-based interface, the tool combines flexibility and accessibility of modern digital platforms, enhancing both educational and research applications.

## Installation (local)
### 1. Clone the repository  
```bash
git clone https://github.com/ChefPoire/BachelorProject
cd Stage_Project
```

### 2. Set up virtual environment and install dependencies:
```bash
uv venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

### 3. Run the app:
```bash
flask run --debug
```
or if you want to run it without debug mode on:
```
python app.py
```
### 4. Open http://localhost:5000 in your browser.

## Project Structure
```
Stage_Project
├─ app.py
├─ processing
│  ├─ slice_processing.py
│  └─ VSItoPNG.py
├─ README.md
├─ requirements.txt
├─ static
│  ├─ images
│  ├─ outputs
│  └─ uploads
└─ templates
   ├─ index.html
   ├─ layout.html
   ├─ result.html
   ├─ slice_preparer.html
   ├─ upload.html
   └─ view_3d.html

```

## License
This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this software with proper attribution.