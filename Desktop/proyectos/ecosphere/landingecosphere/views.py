from django.shortcuts import render
import base64
import uuid
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from .models import Usuario  # As
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from .detection import detect_waste
from django.contrib.auth import authenticate, login

def landing_page(request):
    
    return render(request, 'landing.html')

def registro_view_html(request):
    return render(request, 'registro.html')

def login_view_html(request):
    print("\n=== Iniciando login_view_html ===")
    print(f"Método de la petición: {request.method}")
    print(f"Mensajes: {messages.get_messages(request)}")
    return render(request, 'login.html')

@csrf_exempt
def registro_view(request):
    print("\n=== Iniciando registro_view ===")
    print(f"Método de la petición: {request.method}")
    
    if request.method == 'POST':
        try:
            print("\nDatos recibidos:")
            print(f"POST data: {request.POST}")
            
            usuario = request.POST['usuario']
            contrasena = request.POST['contrasena']
            imagen_base64 = request.POST['imagen_base64']
            
            print(f"Usuario: {usuario}")
            print(f"¿Tiene imagen?: {'Sí' if imagen_base64 else 'No'}")

            # Procesar imagen
            if imagen_base64:
                print("\nProcesando imagen...")
                formato, imgstr = imagen_base64.split(';base64,')
                nombre_archivo = f"{uuid.uuid4()}.jpg"
                print(f"Nombre archivo generado: {nombre_archivo}")
                
                imagen_decodificada = ContentFile(base64.b64decode(imgstr), name=nombre_archivo)
                print("Imagen decodificada correctamente")

                # Guarda usuario
                print("\nCreando nuevo usuario...")
                nuevo_usuario = Usuario(
                    nombre_usuario=usuario,
                    contrasena=contrasena,
                    imagen=imagen_decodificada
                )
                nuevo_usuario.save()
                print("Usuario guardado exitosamente")

                # Agregar mensaje de éxito
                messages.success(request, '¡Registro exitoso! Por favor inicia sesión.')
                print("\nRedirigiendo a login...")
                return redirect('login')
            else:
                print("\nError: No se proporcionó imagen")
                messages.error(request, 'Por favor sube una imagen')
                return render(request, 'registro.html')
                
        except Exception as e:
            print(f"\nError durante el registro: {str(e)}")
            messages.error(request, f'Error en el registro: {str(e)}')
            return render(request, 'registro.html')
            
    print("\nRenderizando formulario de registro")
    return render(request, 'registro.html')

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        
        user = authenticate(request, username=usuario, password=contrasena)
        if user is not None:
            login(request, user)
            # Redirigir al dashboard inmediatamente después del login
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

@csrf_exempt  # Temporalmente desactivamos CSRF para pruebas
def waste_detection(request):
    if request.method == 'POST':
        try:
            image_data = request.POST.get('image_data')
            if image_data:
                result = detect_waste(image_data)
                return JsonResponse(result)
            return JsonResponse({'error': 'No image data provided'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return render(request, 'waste_detection.html')
def waste_detection_html(request):
    return render(request, 'waste_detection.html')

def dashboard(request):
    return render(request, 'dashboard.html')
