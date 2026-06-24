from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from utils import run_inference

app = Flask(**name**)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"wav", "flac", "mp3", "m4a"}

# Create upload directory if it doesn't exist

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
"""Check whether the uploaded file has a supported extension."""
if "." not in filename:
return False

```
extension = filename.rsplit(".", 1)[1].lower()
return extension in ALLOWED_EXTENSIONS
```

@app.route("/")
def home():
return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
uploaded_audio = request.files.get("audio")

```
# Check if a file was selected
if uploaded_audio is None or uploaded_audio.filename == "":
    return render_template(
        "result.html",
        status="error",
        message="❌ No audio file selected."
    )

# Validate file type
if not allowed_file(uploaded_audio.filename):
    return render_template(
        "result.html",
        status="error",
        message="❌ Unsupported audio format."
    )

file_name = secure_filename(uploaded_audio.filename)
file_path = os.path.join(UPLOAD_FOLDER, file_name)

# Save uploaded file temporarily
uploaded_audio.save(file_path)

# Run model inference
result = run_inference(file_path)

# Delete file after prediction
try:
    os.remove(file_path)
except Exception as err:
    print(f"Cleanup failed: {err}")

if result.get("status") == "error":
    return render_template(
        "result.html",
        status="error",
        message=f"❌ Error: {result.get('message', 'Unknown error')}"
    )

prediction = result["label"].upper()
confidence_score = f"{result['confidence']:.4f}"

return render_template(
    "result.html",
    status="success",
    prediction=prediction,
    confidence=confidence_score
)
```

if **name** == "**main**":
app.run(host="0.0.0.0", port=5000)
