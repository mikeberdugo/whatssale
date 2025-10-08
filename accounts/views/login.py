from django.contrib import messages
from accounts.form.login import LoginForm ,PasswordResetForm , PasswordResetTokenForm
from django.shortcuts import render, redirect, get_object_or_404


def Login_view(request):
    

    if request.user.is_authenticated:
        rol = request.session.get('usuario', {}).get('rol')
        return redirect_by_role(rol)
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    complements = {
                        'id': user.id,
                        'rol': user.tipo_user,
                        'name': f"{user.first_name} {user.last_name}",
                        'idempleado': user.id_empleado.idempleado if user.id_empleado else None ,
                        'idempresa': user.id_empresa.first().idempresa if user.id_empresa.count() == 1 else None,
                        'nombre_empresa': user.id_empresa.first().nombreempresa if user.id_empresa.count() == 1 else None
                    }
                    
                    request.session['usuario'] = complements
                    return redirect_by_role(user.tipo_user)
                else:
                    messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            form = LoginForm()
        return render(request, './users/login.html', {'form': form})