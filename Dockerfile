# Usa una imagen base de Python
FROM python:3.10.8

# Establece el directorio de trabajo
WORKDIR /code

# Copia los archivos necesarios al contenedor
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ajusta los permisos de los archivos
RUN chmod -R 777 /code


CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]
