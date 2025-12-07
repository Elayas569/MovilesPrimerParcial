# Imagen base
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto de la app
EXPOSE 8000

# Comando para ejecutar la app
CMD ["python", "app.py"]
