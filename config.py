"""
Configuration file for AgriVision Pro
Adjust these settings to customize the application
"""

# Application Settings
APP_TITLE = "AgriVision Pro - Plant Disease Detection"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Advanced crop disease detection using TensorFlow Lite and PlantVillage Dataset"

# Server Settings
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 8000
DEBUG = False  # Set to True for development
RELOAD = False  # Auto-reload on code changes (development only)

# File Upload Settings
MAX_FILE_SIZE_MB = 5  # Maximum upload size in MB
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'}

# Model Settings
MODEL_PATH = "models/agrivision_edge_model.tflite"
# Note: Input shape is automatically detected from the model
# Typical values: (1, 224, 224, 3) for 224x224 RGB images

# Inference Settings
CONFIDENCE_THRESHOLD = 0.0  # Minimum confidence to display (0.0 to 1.0)
TOP_K_PREDICTIONS = 1  # Number of top predictions to return

# Disease Classes (38 classes from PlantVillage)
DISEASE_CLASSES = {
    # Apple (0-3)
    0: "Apple___Apple_scab",
    1: "Apple___Black_rot",
    2: "Apple___Cedar_apple_rust",
    3: "Apple___healthy",
    
    # Blueberry (4)
    4: "Blueberry___healthy",
    
    # Cherry (5-6)
    5: "Cherry_(including_sour)___Powdery_mildew",
    6: "Cherry_(including_sour)___healthy",
    
    # Corn (7-10)
    7: "Corn_(maize)___Cercospora_leaf_spot_Gray_leaf_spot",
    8: "Corn_(maize)___Common_rust",
    9: "Corn_(maize)___Northern_Leaf_Blight",
    10: "Corn_(maize)___healthy",
    
    # Grape (11-14)
    11: "Grape___Black_rot",
    12: "Grape___Esca_(Black_Measles)",
    13: "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    14: "Grape___healthy",
    
    # Orange (15)
    15: "Orange___Haunglongbing_(Citrus_greening)",
    
    # Peach (16-17)
    16: "Peach___Bacterial_spot",
    17: "Peach___healthy",
    
    # Pepper (18-19)
    18: "Pepper,_bell___Bacterial_spot",
    19: "Pepper,_bell___healthy",
    
    # Potato (20-22)
    20: "Potato___Early_blight",
    21: "Potato___Late_blight",
    22: "Potato___healthy",
    
    # Raspberry (23)
    23: "Raspberry___healthy",
    
    # Soybean (24)
    24: "Soybean___healthy",
    
    # Squash (25)
    25: "Squash___Powdery_mildew",
    
    # Strawberry (26-27)
    26: "Strawberry___Leaf_scorch",
    27: "Strawberry___healthy",
    
    # Tomato (28-37)
    28: "Tomato___Bacterial_spot",
    29: "Tomato___Early_blight",
    30: "Tomato___Late_blight",
    31: "Tomato___Leaf_Mold",
    32: "Tomato___Septoria_leaf_spot",
    33: "Tomato___Spider_mites_Two-spotted_spider_mite",
    34: "Tomato___Target_Spot",
    35: "Tomato___Tomato_mosaic_virus",
    36: "Tomato___Tomato_yellow_leaf_curl_virus",
    37: "Tomato___healthy"
}

# CORS Settings
CORS_ENABLED = False
CORS_ORIGINS = ["http://localhost:3000", "http://localhost:8000"]

# Logging Settings
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "agrivision.log"
ENABLE_FILE_LOGGING = False

# Performance Settings
USE_GPU = False  # Set to True if you have CUDA-capable GPU
NUM_THREADS = 4  # TensorFlow CPU thread count

# Security Settings
VALIDATE_FILE_EXTENSION = True
VALIDATE_FILE_MAGIC_BYTES = False  # Check file header instead of extension
ENABLE_RATE_LIMITING = False
RATE_LIMIT = 100  # Requests per hour

# UI Settings
UI_THEME = "purple"  # Color theme for web interface
SHOW_CONFIDENCE_THRESHOLD_WARNING = True  # Show warning for low confidence
CONFIDENCE_WARNING_THRESHOLD = 0.5  # If confidence below this, show warning

# API Settings
API_PREFIX = "/api"  # API endpoint prefix (use "" for no prefix)
ENABLE_SWAGGER = True  # Enable Swagger docs at /docs
ENABLE_REDOC = True  # Enable ReDoc docs at /redoc
