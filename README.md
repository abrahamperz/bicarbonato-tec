# 📘 Proyecto de Automatización con API de Groq y Google Cloud

Este proyecto utiliza la API de Groq a través de LlamaIndex y servicios de Google Cloud para automatizar tareas desde `script.py`.

---

## 🚀 Requisitos

- Python 3.8 o superior  
- Cuenta en [Groq](https://console.groq.com/)  
- Proyecto configurado en [Google Cloud Console](https://console.cloud.google.com/)  

---

## 🔧 Instalación

1. **Clona este repositorio**

   ```bash
   git clone https://github.com/abrahamperz/bicarbonato-tec
   cd bicarbonato-tec
   ```

2. **Instala las dependencias**

   ```bash
   pip install -r requirements.txt
   ```

---

## 🔑 Configuración

### 1. API Key de Groq

- Ve a [Groq Console](https://console.groq.com/), inicia sesión y genera una nueva API Key.
- Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

  ```env
  GROQ_API_KEY=tu_api_key_aqui
  ```

### 2. Credenciales de Google Cloud

- Entra a [Google Cloud Console](https://console.cloud.google.com/).
- Dirígete a **IAM & Admin > Service Accounts**.
- Crea una nueva cuenta de servicio con permisos necesarios (por ejemplo: acceso a Cloud Storage, Vision AI, etc., según tus necesidades).
- Genera una clave (JSON) y descarga el archivo.
- En tu archivo `script.py`, agrega la siguiente línea para cargar las credenciales:

  ```python
  import os
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ruta/a/tu/archivo_credenciales.json"
  ```

---

## ▶️ Ejecución

Una vez configurado todo correctamente, ejecuta el script principal:

```bash
python script.py
```

```
