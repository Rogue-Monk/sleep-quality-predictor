🌙 AI Sleep Quality Predictor

An interactive Streamlit web app that predicts sleep quality (Good vs Poor) from lifestyle and health metrics.


🚀 Features

✅ AI Model: Random Forest trained on Kaggle Sleep Dataset

✅ Smooth Sliders: Intuitive controls for health/lifestyle inputs

✅ What-if Simulator: Adjust stress, steps, etc. → see how predictions change

✅ Feature Importance: Interactive Plotly chart for transparency

✅ Multi-user Mode: Local session history for different users

✅ Dark/Light Themes with a sidebar toggle

✅ SVG Icons (Next.js style) for modern UI aesthetics


🧩 Tech Stack

Frontend: Streamlit

ML: Scikit-learn, Pandas, Joblib

Visualization: Plotly Express

Icons/UI: Inline SVGs


📂 Project Structure:
.
├── app.py                 # Streamlit app
├── rf_model.pkl           # Trained Random Forest model
├── scaler.pkl             # Fitted StandardScaler
├── feature_columns.pkl    # Feature order for predictions
├── requirements.txt       # Python dependencies
└── README.md              # Project docs


⚡ Installation & Usage

Clone the repo:

git clone https://github.com/your-username/sleep-quality-predictor.git
cd sleep-quality-predictor


Install dependencies:

pip install -r requirements.txt


Run the app:

streamlit run app.py


Open in browser → http://localhost:8501




🧪 Example Inputs

Age: 25

Gender: Male

Sleep Duration: 6.5 hours

Stress Level: 7

Daily Steps: 4000

Heart Rate: 78

BMI: Overweight

Blood Pressure: 140/90

👉 Output: ⚠️ Poor Sleep


📊 Dataset

Trained on Kaggle – Sleep Health and Lifestyle Dataset


🌟 Screenshots



👨‍💻 Author

Your Name (Deek)

📜 License

MIT License © 2025
