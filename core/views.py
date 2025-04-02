from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

# Vista de login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Añadir print para debug
        print(f"Intento de login - Usuario: {username}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {username}!')
            return redirect('home')
        else:
            # Verificar si el usuario existe
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Contraseña incorrecta')
            else:
                messages.error(request, 'El usuario no existe')
            
    return render(request, 'login.html')

# Vista de registro
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validaciones
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return redirect('registro')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado')
            return redirect('registro')

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('registro')

        # Crear nuevo usuario
        try:
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password)
            )
            messages.success(request, 'Usuario registrado exitosamente')
            login(request, user)
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error al registrar usuario: {str(e)}')
            return redirect('registro')

    return render(request, 'registro.html')

# Vista de bienvenida
@login_required
def home_view(request):
    return render(request, 'home.html', {
        'usuario': request.user
    })

# Vista de logout
def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada exitosamente")
    return redirect('login')

# Vista del menú principal
def menu_view(request):
    return render(request, 'menu.html')