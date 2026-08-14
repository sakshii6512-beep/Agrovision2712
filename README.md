# Agrovision2712
to detect and prevent the crop diseases
# AgriVision: Edge-Optimized Deep learning for Real-time Crop Diagnostic 🌾

AgriVision is an advanced Artificial Intelligence system designed to empower farmers with real-time, expert-level plant pathology. By leveraging **Transfer Learning** and **Edge Optimization**, the system can identify 38 different crop diseases across 14 species with high precision, even on low-power mobile devices.

## 📄 Project Documentation

For a full breakdown of the project vision, technical architecture, and future roadmap, visit our official presentation:
👉 **[Project Documentation (Gamma Site)](https://edge-optimized-deep-lear-u5no1vu.gamma.site/)**

---

## 🚀 Key Features

* **38 Disease Classes:** Comprehensive detection across 14 major crops (Tomato, Potato, Apple, Corn, etc.).
* **Explainable AI (XAI):** Integrated **Grad-CAM** technology that highlights exactly where the model sees the disease, building trust with users.
* **Edge Optimization:** Model converted to **TensorFlow Lite (.tflite)** for fast, offline, and battery-efficient performance on mobile/IoT devices.
* **High Accuracy:** Achieved a validation accuracy of **~94.8%** using the MobileNetV2 architecture.

---

## 🛠️ Technical Stack

* **Language:** Python
* **Deep Learning Framework:** TensorFlow / Keras
* **Model Architecture:** MobileNetV2 (Pre-trained on ImageNet)
* **Optimization:** TFLite (Quantization-ready)
* **Dashboard/UI:** Streamlit / Python
* **Dataset:** PlantVillage (54,303 images)

---

## 📊 Evaluation & Metrics

The model was trained for 10 epochs using the **Adam Optimizer** and **Categorical Crossentropy** loss.

| Metric | Value |
| --- | --- |
| **Training Accuracy** | ~96.2% |
| **Validation Accuracy** | ~94.8% |
| **Input Size** | 224 x 224 (RGB) |
| **Model Format** | .h5 (Standard) & .tflite (Edge) |

---

## 🔍 How it Works

1. **Preprocessing:** Leaf images are resized and normalized.
2. **Feature Extraction:** MobileNetV2 identifies patterns (spots, mold, discoloration).
3. **XAI Overlay:** The system generates a heatmap over the original image using Grad-CAM.
4. **Inference:** Near-instant classification results are displayed with a confidence score.

---

## ⚙️ Installation & Usage

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/AgriVision-Edge-XAI.git
cd AgriVision-Edge-XAI

```


2. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


3. **Run the Application:**
```bash
streamlit run app.py

```



---

## 🤝 Contribution

This project was developed for the **Indus AI Week Exhibition**. Contributions to improve accuracy or expand the dataset to local Sindhi crop varieties are welcome!

---

### **Final Tip for GitHub:**

I have mentioned a `requirements.txt` file in the README. To make your repo actually work, create a file named `requirements.txt` in your repo and paste this inside:

```text
tensorflow
numpy
matplotlib
pillow
fastapi
opencv-python

```

**Would you like me to help you write a "Social Media Post" (LinkedIn/Twitter) to share your GitHub repo and Gamma site once you are live?**
