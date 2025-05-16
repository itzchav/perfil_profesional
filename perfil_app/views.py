from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import os
from uuid import uuid4
import joblib
import pandas as pd
from django.conf import settings
import io
from tensorflow.keras.preprocessing.image import img_to_array


def index(request):
    return render(request, 'perfil_app/index.html')
def publicaciones(request):
    return render(request, 'perfil_app/publicaciones.html')
def tesis(request):
    return render(request, 'perfil_app/tesis.html')

def redes(request):
    return render(request, 'perfil_app/redes.html')
def cnn(request):
    context = {}
    model = load_model('mnist_cnn.h5')
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)

    if request.method == 'POST' and request.FILES.get('digit'):
        image = request.FILES['digit']

        # 🧹 Limpiar carpeta media
        for file in os.listdir(fs.location):
            try:
                file_path = os.path.join(fs.location, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print("Error eliminando archivo:", file, e)

        # ✅ Guardar imagen con nombre único
        filename = f"{uuid4().hex}_{image.name}"
        saved_path = fs.save(filename, image)
        full_saved_path = os.path.join(fs.location, saved_path)
        uploaded_file_url = fs.url(saved_path)
        model.summary()

        try:
            # ✅ Procesar imagen
            # Cargar y preprocesar la imagen
            img = Image.open(full_saved_path).convert('L')      # Escala de grises
            img = img.resize((28, 28))                     # Redimensionar a 28x28
            img_array = img_to_array(img)
            img_array = img_array.reshape(1, 28, 28, 1) / 255.0  # Normalizar

            # Predecir
            prediction = model.predict(img_array)
            predicted_digit = np.argmax(prediction)

            print(f"Dígito predicho: {predicted_digit}")
            context = {
                'uploaded_file_url': uploaded_file_url,
                'predicted_digit': predicted_digit
            }

        except Exception as e:
            print("Error procesando la imagen:", e)
            context['error'] = "No se pudo procesar la imagen."
    
    return render(request, 'perfil_app/cnn.html', context)

# Cargar modelo y preprocesador
model = load_model('modelo_precio_autos_mejorado.h5', compile=False)
preprocessor = joblib.load('preprocessor.pkl')

# Columnas usadas por el modelo
categorical_features = ['brand', 'model', 'fuel_type', 'transmission', 'owner_type']
numerical_features = ['year', 'kilometers_driven', 'mileage', 'power', 'engine']
all_features = categorical_features + numerical_features

def regresor(request):
    predicted_price = None

    if request.method == 'POST':
        # Obtener los datos del formulario
        brand = request.POST.get('brand')
        model_name = request.POST.get('model')
        fuel_type = request.POST.get('fuel_type')
        transmission = request.POST.get('transmission')
        owner_type = request.POST.get('owner_type')
        year = int(request.POST.get('year'))
        kilometers = int(request.POST.get('kilometers_driven'))
        mileage = float(request.POST.get('mileage'))
        engine = int(request.POST.get('engine'))
        power = float(request.POST.get('power'))

        # Datos de entrada
        input_data = {
            "brand": brand,
            "model": model_name,
            "fuel_type": fuel_type,
            "transmission": transmission,
            "year": year,
            "kilometers_driven": kilometers,
            "mileage": mileage,
            "engine": engine,
            "power": power,
            "owner_type": owner_type
        }

        # Crear DataFrame
        input_df = pd.DataFrame([input_data])

        # Asegurar que las columnas estén en el orden esperado
        input_df = input_df[all_features]

        # Preprocesar los datos
        X_input_scaled = preprocessor.transform(input_df)

        # Realizar la predicción
        predicted_price = np.expm1(model.predict(X_input_scaled)[0][0])

    return render(request, 'perfil_app/regresor.html', {
        'predicted_price': predicted_price
    })