# EduWord

Plataforma educativa desarrollada en Python orientada al aprendizaje interactivo para niños y la gestión de actividades por parte del docente. Incluye herramientas educativas, juegos interactivos y un sistema de generación de certificados digitales con firma criptográfica.

---

##  Funcionalidades principales

### Para Maestros
- Generación de certificados digitales para alumnos
- Sistema de autenticación de documentos mediante **firma digital (criptografía asimétrica)**
- Creación de llaves pública y privada para validación de certificados
- Gestión de información de alumnos

### Para Alumnos
- Juego tipo memorama educativo
- Lector de códigos QR
- Lector de texto
- Glosario interactivo de palabras

---

## Sistema de seguridad

El sistema de certificados utiliza **criptografía asimétrica**, donde:

- La **clave privada** es utilizada por el sistema para firmar certificados
- La **clave pública** permite validar la autenticidad del documento

Esto asegura que los certificados no puedan ser modificados sin invalidar su firma.

- Encriptación de contraseñas en la base de datos

---

## Tecnologías utilizadas
- Python
- Tkinter
- Firebase Firestore
- OpenCV (si aplica QR)
- Librerías de criptografía (firma digital)

---

## Instalación

```bash
git clone https://github.com/Daniela0109/EduWord.git
cd EduWord
pip install -r requirements.txt
python app.py
```

---

## Lo que aprendí
- Desarrollo de interfaces con Tkinter
- Integración con Firebase
- Manejo de datos en tiempo real
- Implementación de criptografía asimétrica para validación de documentos

---

## Mejoras futuras
- Migración a aplicación web o móvil
- Sistema de progreso por alumno
- Mejoras en UI/UX
- Base de datos más escalable
