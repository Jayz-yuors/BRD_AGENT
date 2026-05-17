import joblib

# -------------------------------
# LOAD MODELS
# -------------------------------
DET_MODEL_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\ml_models\requirement_detector\model.pkl"
DET_VEC_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\ml_models\requirement_detector\vectorizer.pkl"

CLS_MODEL_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\ml_models\requirement_classifier\model.pkl"
CLS_VEC_PATH = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\ml_models\requirement_classifier\vectorizer.pkl"


det_model = joblib.load(DET_MODEL_PATH)
det_vectorizer = joblib.load(DET_VEC_PATH)

cls_model = joblib.load(CLS_MODEL_PATH)
cls_vectorizer = joblib.load(CLS_VEC_PATH)


# -------------------------------
# DETECT REQUIREMENT
# -------------------------------
def is_requirement(text):

    X = det_vectorizer.transform([text])
    pred = det_model.predict(X)[0]

    return pred == 1


# -------------------------------
# CLASSIFY TYPE
# -------------------------------
def classify_requirement(text):

    X = cls_vectorizer.transform([text])
    pred = cls_model.predict(X)[0]

    return "Non-Functional" if pred == 1 else "Functional"