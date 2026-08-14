# 🚀 Quick Start Guide - AgriVision Pro

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Verify Setup
```bash
python verify_setup.py
```

### Step 3: Run Application
```bash
python main.py
```

### Step 4: Access Web Interface
Open your browser and go to:
```
http://localhost:8000
```

---

## 📸 How to Use

1. **Upload Plant Image**
   - Click the upload area or drag-and-drop
   - Supported: JPG, PNG, GIF (Max 5MB)

2. **Click "Initialize Scan"**
   - Wait for analysis to complete
   - Usually takes 1-5 seconds

3. **View Results**
   - See detected plant and disease
   - Check confidence score
   - **Read treatment recommendations** 💊 (displayed below the Initialize Scan button)

---

## 🎯 Key Features

### Disease Detection
- **38 Plant Disease Classes** from PlantVillage dataset
- Real-time predictions
- Confidence scoring

### Treatment Recommendations
Each detected disease includes:
- ✓ Fungicide/pesticide recommendations
- ✓ Application schedules and frequencies
- ✓ Cultural practices and pruning tips
- ✓ Preventive measures
- ✓ Environmental management

### Example Output
**Detected**: Tomato - Early Blight  
**Confidence**: 92.34%  
**Treatment**:
- Apply fungicide (Chlorothalonil or Mancozeb) starting at first branch
- Repeat every 7-10 days
- Remove lower infected leaves
- Improve air circulation
- Use drip irrigation instead of overhead
- Plant certified disease-free seeds
- Avoid working in wet fields

---

## 🔧 Troubleshooting

### Issue: Port 8000 already in use
**Solution**:
```bash
python -m uvicorn main:app --port 8001
```

### Issue: Model not found
**Solution**: Make sure the model file exists:
```
models/agrivision_edge_model.tflite
```

### Issue: Dependencies not installing
**Solution**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Import errors
**Solution**:
```bash
python -m pip install tensorflow pillow numpy fastapi uvicorn python-multipart
```

---

## 📡 API Usage (Advanced)

### Using cURL
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -F "file=@tomato_leaf.jpg"
```

### Using Python
```python
import requests

with open('tomato_leaf.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/predict', files=files)
    result = response.json()
    
    print(f"Plant: {result['plant']}")
    print(f"Disease: {result['disease']}")
    print(f"Confidence: {result['confidence_percentage']}")
    print("\nTreatment:")
    for i, treatment in enumerate(result['treatment'], 1):
        print(f"{i}. {treatment}")
```

### Using Node.js/Fetch
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/predict', {
    method: 'POST',
    body: formData
})
.then(r => r.json())
.then(data => {
    console.log('Plant:', data.plant);
    console.log('Disease:', data.disease);
    console.log('Treatment:', data.treatment);
});
```

---

## 🌍 Deploy to Cloud

### Deploy to Heroku (Free tier available)
```bash
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git push heroku main
```

### Deploy to Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway up
```

### Deploy with Docker
```bash
# Build image
docker build -t agrivision .

# Run container
docker run -p 8000:8000 agrivision
```

---

## ℹ️ System Requirements

- **Python**: 3.8+
- **Memory**: 2GB minimum
- **Disk**: 500MB minimum
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

---

## 📞 Support

For issues:
1. Run `python verify_setup.py` to check configuration
2. Check browser console for JavaScript errors
3. Review terminal output for Python errors
4. Ensure model file exists and is accessible

---

## 🔐 Security Tips

- Run on trusted networks only
- Don't expose to untrusted internet without authentication
- Validate image file types server-side (already done)
- Limit file upload size (5MB max)
- Use HTTPS in production

---

**Happy farming! 🌾**  
AgriVision Pro v1.0
