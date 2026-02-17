imageutils.py is a library that holds function for creating image vectors
genutils.py is a library with one function that parses command-line params into a dict
supportFuncs.py holds functions for training and testing data
ImageClass.py holds the class data for images
ImageClass_helper.py holds the helper functions for the ImageClass class
main.py has the main functions that is run from parsing a commandline script

To run the program:
Required: enter the the directory to the training and testing sets of classes that hold images for those classes.
Optional: enter image size, number of classes (2-10), and threshold percent
Expected Usage: python main.py training_set_path='<directory>' testing_set_path='<directory>' [img_size=<value> num_classes=<value> threshold=<value>]

---

## Dataset folder structure (required)

Both the training and testing directories must contain **one subfolder per class**, and each class folder must contain `.jpg` / `.jpeg` images.

Example:

- training_set_path/
  - cats/
    - cat.1.jpg
  - dogs/
    - dog.1.jpg
- testing_set_path/
  - cats/
    - cat.4001.jpg
  - dogs/
    - dog.4001.jpg

---

## Web UI (folder upload)

This repo includes a small web UI (Next.js) + a Python API so you can:

- upload a **training** folder into the "Training Images" box
- upload a **test** folder into the "Test Images" box
- click **Start Training Classifier** to run the same training/testing logic and see accuracy in the browser

### Start the backend API

From this folder (`Image-Classifier/`):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

### Start the frontend

From the repo root:

```bash
cd web
npm install
npm run dev
```

Open `http://localhost:3000`.

### Notes

- Folder upload works best in Chromium browsers (Chrome/Edge) because it relies on the browser providing relative paths for uploaded files.
- If your backend is not on `http://localhost:8000`, set `NEXT_PUBLIC_API_URL` before running the frontend.
