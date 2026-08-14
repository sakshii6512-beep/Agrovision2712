from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
from pathlib import Path

app = FastAPI(title="AgriVision Pro - Plant Disease Detection")

# PlantVillage Dataset - 38 Classes with Treatments
PLANT_DISEASES = {
    0: {
        "name": "Apple - Apple Scab",
        "plant": "Apple",
        "disease": "Apple Scab",
        "treatment": [
            "Apply fungicide spray (Sulfur or Mancozeb) at 2-week intervals",
            "Remove and destroy infected leaves and branches",
            "Improve air circulation by pruning dense branches",
            "Avoid overhead watering to reduce leaf wetness",
            "Use disease-resistant apple varieties",
            "Sanitize pruning tools between cuts"
        ]
    },
    1: {
        "name": "Apple - Black Rot",
        "plant": "Apple",
        "disease": "Black Rot",
        "treatment": [
            "Remove infected fruit and branches (cut 6 inches below affected area)",
            "Apply fungicide containing Captan or Thiophanate-methyl",
            "Prune to improve air circulation",
            "Sterilize pruning equipment",
            "Maintain proper orchard sanitation",
            "Remove canker lesions during winter dormancy"
        ]
    },
    2: {
        "name": "Apple - Cedar Apple Rust",
        "plant": "Apple",
        "disease": "Cedar Apple Rust",
        "treatment": [
            "Apply sulfur-based fungicide weekly from green tip stage",
            "Use mancozeb or myclobutanil during critical periods",
            "Remove alternate hosts (Eastern Red Cedar/Juniper)",
            "Provide good air circulation through pruning",
            "Apply fungicide every 7-10 days during wet springs",
            "Plant resistant apple varieties"
        ]
    },
    3: {
        "name": "Apple - Healthy",
        "plant": "Apple",
        "disease": "Healthy",
        "treatment": [
            "No treatment needed",
            "Continue regular maintenance pruning",
            "Monitor regularly for signs of disease",
            "Apply preventive fungicide spray schedule if in high-risk area",
            "Maintain proper fertilization and irrigation"
        ]
    },
    4: {
        "name": "Blueberry - Healthy",
        "plant": "Blueberry",
        "disease": "Healthy",
        "treatment": [
            "No treatment needed",
            "Maintain proper pH (4.5-5.5)",
            "Regular pruning to maintain plant vigor",
            "Monitor for pest and disease symptoms",
            "Ensure adequate drainage"
        ]
    },
    5: {
        "name": "Cherry - Powdery Mildew",
        "plant": "Cherry",
        "disease": "Powdery Mildew",
        "treatment": [
            "Apply sulfur spray or potassium bicarbonate",
            "Use horticultural oil combined with fungicide",
            "Improve air circulation by pruning",
            "Avoid over-watering",
            "Remove heavily infected branches",
            "Apply treatment at first signs of disease"
        ]
    },
    6: {
        "name": "Cherry - Healthy",
        "plant": "Cherry",
        "disease": "Healthy",
        "treatment": [
            "No treatment needed",
            "Continue regular pruning and maintenance",
            "Monitor for early disease signs",
            "Ensure proper irrigation during dry periods",
            "Apply preventive measures if necessary"
        ]
    },
    7: {
        "name": "Corn - Cercospora Leaf Spot / Gray Leaf Spot",
        "plant": "Corn",
        "disease": "Cercospora Leaf Spot / Gray Leaf Spot",
        "treatment": [
            "Plant resistant corn hybrids",
            "Apply fungicide (Strobilurin or Triazole) at V6-V8 growth stage",
            "Rotate crops with non-host plants for 2-3 years",
            "Remove and destroy crop residue",
            "Maintain proper plant spacing for air circulation",
            "Monitor field regularly starting at V4 growth stage"
        ]
    },
    8: {
        "name": "Corn - Common Rust",
        "plant": "Corn",
        "disease": "Common Rust",
        "treatment": [
            "Plant disease-resistant corn hybrids",
            "Apply fungicide if >5% of leaf area is affected",
            "Use Triazole or Strobilurin fungicides",
            "Eliminate volunteer corn plants",
            "Destroy crop residue after harvest",
            "Monitor fields during growth season"
        ]
    },
    9: {
        "name": "Corn - Northern Leaf Blight",
        "plant": "Corn",
        "disease": "Northern Leaf Blight",
        "treatment": [
            "Plant resistant corn varieties",
            "Apply preventive fungicide at V6-V8 stage",
            "Use products containing Strobilurin or Triazole",
            "Improve air circulation and reduce excess nitrogen",
            "Rotate crops for 2+ years",
            "Monitor weather for conditions favoring disease (cool, wet)"
        ]
    },
    10: {
        "name": "Corn - Healthy",
        "plant": "Corn",
        "disease": "Healthy",
        "treatment": [
            "No treatment needed",
            "Continue regular monitoring",
            "Apply preventive fungicide if disease pressure is high in area",
            "Maintain proper fertilization",
            "Ensure adequate irrigation"
        ]
    },
    11: {
        "name": "Grape - Black Rot",
        "plant": "Grape",
        "disease": "Black Rot",
        "treatment": [
            "Remove and destroy infected berries and shoots",
            "Apply fungicide (Mancozeb or Captan) every 7-10 days",
            "Start fungicide applications at bloom",
            "Continue through fruit development",
            "Prune to improve air circulation",
            "Clean up fallen fruit and debris regularly"
        ]
    },
    12: {
        "name": "Grape - Esca (Black Measles)",
        "plant": "Grape",
        "disease": "Esca (Black Measles)",
        "treatment": [
            "No cure available - remove and destroy infected vines",
            "Avoid pruning in wet weather",
            "Sterilize pruning tools with 70% ethanol",
            "Fill pruning wounds with wound dressing",
            "Improve vine vigor through proper nutrition",
            "Plant from certified disease-free nursery stock"
        ]
    },
    13: {
        "name": "Grape - Leaf Blight (Isariopsis Leaf Spot)",
        "plant": "Grape",
        "disease": "Leaf Blight / Isariopsis Leaf Spot",
        "treatment": [
            "Remove infected leaves and shoots",
            "Apply fungicide (Mancozeb or Sulfur) weekly",
            "Improve air circulation through proper pruning",
            "Avoid overhead irrigation",
            "Clean up fallen leaves and debris",
            "Space plants for maximum air flow"
        ]
    },
    14: {
        "name": "Grape - Healthy",
        "plant": "Grape",
        "disease": "Healthy",
        "treatment": [
            "No treatment needed",
            "Continue preventive fungicide sprays if disease pressure remains",
            "Regular pruning and leaf removal",
            "Monitor for disease symptoms",
            "Maintain proper canopy management"
        ]
    },
    15: {
        "name": "Orange - Huanglongbing (Citrus Greening)",
        "plant": "Orange",
        "disease": "Huanglongbing (Citrus Greening)",
        "treatment": [
            "No cure - remove and destroy infected trees",
            "Control Asian citrus psyllid vector with insecticides",
            "Use yellow sticky traps to monitor psyllid populations",
            "Cut off infected branches immediately",
            "Maintain good tree vigor with proper fertilization",
            "Plant disease-free nursery stock",
            "Implement strict quarantine measures"
        ]
    },
    16: {
        "name": "Peach - Bacterial Spot",
        "plant": "Peach",
        "disease": "Bacterial Spot",
        "treatment": [
            "Apply copper-based bactericide at bud break and bloom",
            "Use fixed copper or basic copper sulfate",
            "Repeat applications every 7-10 days during wet weather",
            "Remove infected branches and fruit",
            "Sterilize pruning tools between cuts",
            "Avoid overhead irrigation",
            "Plant resistant varieties if available"
        ]
    },
    17: {
        "name": "Peach - Healthy",
        "plant": "Peach",
        "disease": "Healthy",
        "treatment": [
            "No treatment needed",
            "Continue regular monitoring",
            "Apply preventive copper spray at bud break if in high-risk area",
            "Maintain proper tree structure through pruning",
            "Ensure adequate irrigation"
        ]
    },
    18: {
        "name": "Pepper (Bell) - Bacterial Spot",
        "plant": "Pepper",
        "disease": "Bacterial Spot",
        "treatment": [
            "Remove infected plants immediately",
            "Apply copper fungicide/bactericide weekly",
            "Use resistant pepper varieties",
            "Avoid overhead watering and working in wet foliage",
            "Sterilize greenhouse and equipment",
            "Improve air circulation with fans",
            "Practice crop rotation"
        ]
    },
    19: {
        "name": "Pepper (Bell) - Healthy",
        "plant": "Pepper",
        "disease": "Healthy",
        "treatment": [
            "No treatment needed",
            "Continue regular monitoring",
            "Maintain proper spacing for air circulation",
            "Monitor soil moisture",
            "Apply preventive copper spray if disease appears in area"
        ]
    },
    20: {
        "name": "Potato - Early Blight",
        "plant": "Potato",
        "disease": "Early Blight",
        "treatment": [
            "Apply fungicide (Chlorothalonil or Mancozeb) starting at first branch",
            "Repeat every 7-10 days, more frequently in wet weather",
            "Remove lower infected leaves manually",
            "Improve air circulation by removing lower foliage",
            "Use drip irrigation instead of overhead",
            "Plant certified disease-free seed potatoes",
            "Avoid working in field when wet"
        ]
    },
    21: {
        "name": "Potato - Late Blight",
        "plant": "Potato",
        "disease": "Late Blight",
        "treatment": [
            "Apply fungicide (Metalaxyl+Chlorothalonil) at first sign of disease",
            "Spray every 5-7 days during cool, wet periods",
            "Improve air circulation and reduce humidity",
            "Use drip irrigation instead of overhead",
            "Remove and destroy infected plants",
            "Plant resistant potato varieties",
            "Avoid overhead irrigation and working in wet fields",
            "Destroy potato cull piles"
        ]
    },
    22: {
        "name": "Potato - Healthy",
        "plant": "Potato",
        "disease": "Healthy",
        "treatment": [
            "No treatment needed",
            "Continue monitoring for disease symptoms",
            "Apply preventive fungicide if weather favors disease",
            "Maintain proper spacing and remove lower leaves",
            "Use proper irrigation practices"
        ]
    },
    23: {
        "name": "Raspberry - Healthy",
        "plant": "Raspberry",
        "disease": "Healthy",
        "treatment": [
            "No treatment needed",
            "Regular pruning to remove old canes",
            "Monitor for pest and disease symptoms",
            "Maintain proper row spacing",
            "Ensure adequate drainage"
        ]
    },
    24: {
        "name": "Soybean - Healthy",
        "plant": "Soybean",
        "disease": "Healthy",
        "treatment": [
            "No treatment needed",
            "Continue regular crop monitoring",
            "Apply foliar fungicide if disease pressure increases",
            "Maintain proper plant population",
            "Monitor soil moisture"
        ]
    },
    25: {
        "name": "Squash - Powdery Mildew",
        "plant": "Squash",
        "disease": "Powdery Mildew",
        "treatment": [
            "Apply sulfur fungicide or potassium bicarbonate spray",
            "Use horticultural oil with neem oil",
            "Spray every 7-10 days starting at first sign",
            "Improve air circulation by removing affected leaves",
            "Water at soil level to keep foliage dry",
            "Plant resistant varieties",
            "Space plants properly for air flow"
        ]
    },
    26: {
        "name": "Strawberry - Leaf Scorch",
        "plant": "Strawberry",
        "disease": "Leaf Scorch",
        "treatment": [
            "Remove and destroy infected leaves",
            "Apply fungicide (Captan or Sulfur) at first sign",
            "Repeat sprays every 7-10 days",
            "Improve air circulation with proper spacing",
            "Avoid overhead watering",
            "Remove runners if necessary to reduce spread",
            "Clean up infected foliage regularly"
        ]
    },
    27: {
        "name": "Strawberry - Healthy",
        "plant": "Strawberry",
        "disease": "Healthy",
        "treatment": [
            "No treatment needed",
            "Continue regular monitoring",
            "Remove dead or damaged foliage",
            "Maintain proper spacing and remove runners",
            "Monitor soil moisture"
        ]
    },
    28: {
        "name": "Tomato - Bacterial Spot",
        "plant": "Tomato",
        "disease": "Bacterial Spot",
        "treatment": [
            "Remove infected plants if disease is severe",
            "Apply copper-based bactericide weekly",
            "Use fixed copper or basic copper sulfate",
            "Avoid overhead watering and working in wet foliage",
            "Sterilize tools, stakes, cages, and trellises",
            "Use certified disease-free seeds",
            "Plant resistant tomato varieties"
        ]
    },
    29: {
        "name": "Tomato - Early Blight",
        "plant": "Tomato",
        "disease": "Early Blight",
        "treatment": [
            "Remove lower diseased leaves as they appear",
            "Apply fungicide (Chlorothalonil or Mancozeb) every 7-10 days",
            "Space plants for good air circulation",
            "Use drip irrigation instead of overhead",
            "Mulch around base to prevent soil splash",
            "Avoid working in field when wet",
            "Clean up plant debris after harvest"
        ]
    },
    30: {
        "name": "Tomato - Late Blight",
        "plant": "Tomato",
        "disease": "Late Blight",
        "treatment": [
            "Remove infected plants and fruit immediately",
            "Destroy plant material and do not compost",
            "Apply fungicide (Chlorothalonil+Metalaxyl) starting at first sign",
            "Spray every 5-7 days during cool, wet weather",
            "Improve air circulation by removing leaves",
            "Use resistant tomato varieties",
            "Avoid overhead irrigation"
        ]
    },
    31: {
        "name": "Tomato - Leaf Mold",
        "plant": "Tomato",
        "disease": "Leaf Mold",
        "treatment": [
            "Apply fungicide (Chlorothalonil or Sulfur) at first sign",
            "Repeat every 7-10 days",
            "Improve air circulation through proper pruning",
            "Avoid overhead watering",
            "Use drip irrigation",
            "Reduce humidity by increasing ventilation",
            "Space plants properly",
            "Remove lower infected leaves"
        ]
    },
    32: {
        "name": "Tomato - Septoria Leaf Spot",
        "plant": "Tomato",
        "disease": "Septoria Leaf Spot",
        "treatment": [
            "Remove diseased leaves immediately",
            "Apply fungicide starting at first symptom",
            "Use Chlorothalonil, Mancozeb, or Copper-based products",
            "Spray every 7-10 days, more frequently in wet weather",
            "Improve air circulation by pruning",
            "Use drip irrigation to keep foliage dry",
            "Sanitize tools between plants",
            "Practice crop rotation (don't plant tomato in same area for 2-3 years)"
        ]
    },
    33: {
        "name": "Tomato - Spider Mites (Two-spotted Spider Mite)",
        "plant": "Tomato",
        "disease": "Spider Mites",
        "treatment": [
            "Spray with water to dislodge mites",
            "Apply miticide (Abamectin or Neem oil) if needed",
            "Monitor leaves carefully, especially undersides",
            "Increase humidity to discourage population growth",
            "Remove heavily infested leaves",
            "Introduce natural predators (phytoseiid mites)",
            "Avoid excessive nitrogen fertilization"
        ]
    },
    34: {
        "name": "Tomato - Target Spot",
        "plant": "Tomato",
        "disease": "Target Spot",
        "treatment": [
            "Remove diseased leaves and destroyed affected plant parts",
            "Apply fungicide (Chlorothalonil, Mancozeb, or Copper) at first sign",
            "Spray every 7-10 days, more frequently in wet conditions",
            "Improve air circulation through pruning",
            "Use drip irrigation to avoid wet foliage",
            "Sanitize tools between cuts",
            "Practice crop rotation",
            "Avoid overcrowding plants"
        ]
    },
    35: {
        "name": "Tomato - Tomato Mosaic Virus",
        "plant": "Tomato",
        "disease": "Tomato Mosaic Virus",
        "treatment": [
            "Remove and destroy infected plants immediately",
            "Wash hands and sanitize tools with 10% bleach solution",
            "Use virus-resistant tomato varieties",
            "Control aphids and thrips (virus vectors)",
            "Don't work in field when plants are wet",
            "Remove weeds that may harbor virus",
            "Use certified virus-free seeds",
            "Implement strict quarantine of diseased plants"
        ]
    },
    36: {
        "name": "Tomato - Tomato Yellow Leaf Curl Virus",
        "plant": "Tomato",
        "disease": "Tomato Yellow Leaf Curl Virus",
        "treatment": [
            "Remove and destroy infected plants immediately",
            "Control whitefly vectors with insecticide",
            "Use yellow sticky traps to monitor whitefly",
            "Plant resistant tomato varieties",
            "Remove infected weeds around field",
            "Use fine mesh netting to exclude whiteflies",
            "Avoid overhead watering",
            "Do not work in infected field and then healthy field"
        ]
    },
    37: {
        "name": "Tomato - Healthy",
        "plant": "Tomato",
        "disease": "Healthy",
        "treatment": [
            "No treatment needed",
            "Continue regular monitoring for disease symptoms",
            "Maintain proper plant spacing and pruning",
            "Use drip irrigation and avoid wetting foliage",
            "Apply preventive fungicide if disease pressure increases in area"
        ]
    }
}

# Load the TFLite model
MODEL_PATH = "models/agrivision_edge_model.tflite"

try:
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    input_shape = input_details[0]['shape']
    IMG_HEIGHT = input_shape[1]
    IMG_WIDTH = input_shape[2]
    
    print(f"Model loaded successfully. Input shape: {input_shape}")
except Exception as e:
    print(f"Error loading model: {e}")
    interpreter = None

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict plant disease from uploaded image
    """
    try:
        if interpreter is None:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Preprocess image
        image = image.convert('RGB')
        image = image.resize((IMG_WIDTH, IMG_HEIGHT))
        image_array = np.array(image, dtype=np.float32)
        
        # Normalize if needed (adjust based on your model training)
        image_array = image_array / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        # Run inference
        interpreter.set_tensor(input_details[0]['index'], image_array)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        
        # Get prediction
        predictions = output_data[0]
        predicted_class = np.argmax(predictions)
        confidence = float(predictions[predicted_class])
        
        # Get disease information
        disease_info = PLANT_DISEASES.get(predicted_class, {
            "name": "Unknown",
            "plant": "Unknown",
            "disease": "Unknown",
            "treatment": ["Unable to determine treatment"]
        })
        
        return JSONResponse({
            "success": True,
            "class": int(predicted_class),
            "confidence": float(confidence),
            "plant": disease_info["plant"],
            "disease": disease_info["disease"],
            "full_name": disease_info["name"],
            "confidence_percentage": f"{confidence * 100:.2f}%",
            "treatment": disease_info["treatment"]
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=400)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": interpreter is not None,
        "total_classes": len(PLANT_DISEASES)
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🌿 AgriVision Pro - Starting...")
    print("="*60)
    print("📱 Web Interface: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("="*60 + "\n")
    
    # host="0.0.0.0" listens on all interfaces but use localhost to access
    # For network access from other machines, change host to your machine IP
    uvicorn.run(app, host="127.0.0.1", port=8000)
