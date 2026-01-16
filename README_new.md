# Bachelor Project Psychobiology: <br>3D Brain Imaging Project

## Description
**BankjeMaps** is a mobile-friendly web app that helps people discover, enjoy, and share public benches ("bankjes") in their environment.

### What does it do?
BankjeMaps makes it easy to:
- find nearby bankjes on an interactive map
- view photos, descriptions, and names of bankjes
- Add new bankjes with images and descriptions
- Rate or favourite bankjes to keep track of the best spots

### How does it work?
- Users can **log in** or **register** for an account to access the platform.
- Upon login, users are shown a dynamic map of nearby bankjes.
- Each bankje has a **detail page** with its name, user-submitted rating, description, and photos.
- Users can **add new bankjes** via a form that collects a name, description, photo, and location.
- New photo uploads are **moderated** by the community before appearing on the map.
- Users can **rate bankjes** or **mark them as favourites** for easy access later.

### Target Audience
BankjeMaps is for **anyone looking to relax outside**, wheter during a walk, bike ride, or while exploring a city. Because the app is mainly accessed on-the-go, it is optimized for **mobile use**.

### Why BankjeMaps?
While apps like [benchfinder.ch](https://benchfinder.ch) exist, they **lack features** like photos, descriptions, ratings, or community-driven contributions.  
BankjeMaps fills this gap by allowing:
- Full bench pages with names, images, and details
- Users to "discover" a bench and give it a name (e.g., “Discovered by [username]”)
- A user-friendly, IMDB-style rating system
- Community-based moderation to ensure valid content

## Tech Stack
- **Frontend:** HTML, Bootstrap, Leaflet.js
- **Backend:** Flask (Python)
- **Database:** PostgreSQL
- **Additional Tools:** JavaScript for map interactivity

## Screenshots and DemoVideo
### Light Mode
<img src="static/Images/MockUps/mockup_light_1.png" alt="Mockup Light 1" width="250"/>
<img src="static/Images/MockUps/mockup_light_2.png" alt="Mockup Light 2" width="250"/>

### Dark Mode
<img src="static/Images/MockUps/mockup_dark_1.png" alt="Mockup Dark 1" width="250"/>
<img src="static/Images/MockUps/mockup_dark_2.png" alt="Mockup Dark 2" width="250"/>

### Other examples
<img src="static/Images/MockUps/mockup_dark_start.png" alt="Mockup Dark Start" width="250">
<img src="static/Images/MockUps/mockup_dark_profile.png" alt="Mockup Dark Profile" width="250">

### Demo Video
<video width="250" controls>
  <source src="static/BankjeMaps_DemoVideo.mp4" type="video/mp4">
</video>

## Installation (local)
### 1. Clone the repository  
```bash
git clone https://github.com/minprog-platforms/project-ChefPoire
cd BankjeMaps
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

### 4. Open http://localhost:5000 in your browser.

## Roadmap / Future Features
- User profiles with profile photos
- Friend system to see each other's favorite bankjes
- Review system for rating bankjes with additional comments
- More detailed moderation dashboard
- Tagging features (e.g., "shady", "quiet", "great view", "trash can close-by")

## Developed by
Peer ten Klooster<br>
Minor Programmeren Project<br>
University of Amsterdam

## License
This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this software with proper attribution.

## References & Acknowledgements
This project was developed as part of the Minor Programmeren at the University of Amsterdam.

Special thanks to the following tools, libraries, and resources that made this project possible:

- Brian Yu and David Malan, CSCI S-33a at Harvard, published 2019 under a Creative Commons Attribution-Noncommercial-Share Alike 3.0 Unported license.
- David Malan, CS164 at Harvard, published 2012 under a Creative Commons Attribution-Noncommercial-Share Alike 3.0 Unported license.
- Flask – for powering the Python backend.
- Leaflet.js – for the interactive maps and marker functionality.
- Bootstrap – for responsive frontend components and layout.
- Flaticon – for providing icons.
- SQLite – for simple and lightweight database management.
- Jinja2 – for rendering dynamic HTML templates.
- OpenStreetMap – for map tile data used with Leaflet.
- JawgLab - for additional map tile data used with Leaflet.
- Inspiration for the project idea was drawn from sites like benchfinder.ch.
- overpass-turbo.eu - for GeoJson data used to create marker data used with Leaflet.
- UIverse.io - for the theme toggler in the navigation bar.

Additional thanks to:
- Fellow students and instructors at UvA for their guidance and feedback.