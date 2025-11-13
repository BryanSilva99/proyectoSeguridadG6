#!/usr/bin/env python
"""
Script de prueba para el sistema de autenticación JWT
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_response(response, title):
    """Imprime la respuesta de manera formateada"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_authentication():
    """Prueba el flujo completo de autenticación"""
    
    print("\n🧪 INICIANDO PRUEBAS DE AUTENTICACIÓN JWT")
    
    # 1. Registro de nuevo usuario (cliente)
    print("\n1️⃣ Registro de nuevo usuario...")
    register_data = {
        "username": "test_cliente",
        "password": "TestPassword123!",
        "email": "test@example.com",
        "dni": "99999999",
        "full_name": "Usuario de Prueba",
        "address": "Calle Test 123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
    print_response(response, "1. REGISTRO DE USUARIO")
    
    if response.status_code == 201:
        data = response.json()
        access_token = data['access']
        refresh_token = data['refresh']
        print("✅ Registro exitoso")
    else:
        print("❌ Error en el registro")
        return
    
    # 2. Login con credenciales
    print("\n2️⃣ Login con credenciales...")
    login_data = {
        "username": "test_cliente",
        "password": "TestPassword123!"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    print_response(response, "2. LOGIN")
    
    if response.status_code == 200:
        data = response.json()
        access_token = data['access']
        refresh_token = data['refresh']
        print("✅ Login exitoso")
    else:
        print("❌ Error en el login")
        return
    
    # 3. Verificar token
    print("\n3️⃣ Verificando token...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(f"{BASE_URL}/auth/verify/", headers=headers)
    print_response(response, "3. VERIFICAR TOKEN")
    
    if response.status_code == 200:
        print("✅ Token válido")
    else:
        print("❌ Token inválido")
    
    # 4. Obtener usuario actual
    print("\n4️⃣ Obteniendo usuario actual...")
    response = requests.get(f"{BASE_URL}/auth/me/", headers=headers)
    print_response(response, "4. USUARIO ACTUAL")
    
    if response.status_code == 200:
        print("✅ Usuario obtenido correctamente")
    else:
        print("❌ Error al obtener usuario")
    
    # 5. Acceder a endpoint protegido (lista de libros)
    print("\n5️⃣ Accediendo a endpoint protegido (libros)...")
    response = requests.get(f"{BASE_URL}/libros/", headers=headers)
    print_response(response, "5. LISTA DE LIBROS (PROTEGIDO)")
    
    if response.status_code == 200:
        print("✅ Acceso exitoso a endpoint protegido")
    else:
        print("❌ Error al acceder a endpoint protegido")
    
    # 6. Refrescar token
    print("\n6️⃣ Refrescando token...")
    refresh_data = {"refresh": refresh_token}
    
    response = requests.post(f"{BASE_URL}/auth/refresh/", json=refresh_data)
    print_response(response, "6. REFRESCAR TOKEN")
    
    if response.status_code == 200:
        data = response.json()
        new_access_token = data['access']
        new_refresh_token = data['refresh']
        print("✅ Token refrescado exitosamente")
        access_token = new_access_token
        refresh_token = new_refresh_token
    else:
        print("❌ Error al refrescar token")
    
    # 7. Logout
    print("\n7️⃣ Cerrando sesión...")
    headers = {"Authorization": f"Bearer {access_token}"}
    logout_data = {"refresh": refresh_token}
    
    response = requests.post(f"{BASE_URL}/auth/logout/", json=logout_data, headers=headers)
    print_response(response, "7. LOGOUT")
    
    if response.status_code == 200:
        print("✅ Logout exitoso")
    else:
        print("❌ Error en logout")
    
    # 8. Intentar usar token después del logout
    print("\n8️⃣ Intentando usar token después del logout...")
    response = requests.get(f"{BASE_URL}/auth/verify/", headers=headers)
    print_response(response, "8. VERIFICAR TOKEN DESPUÉS DE LOGOUT")
    
    # El access token todavía puede ser válido si no ha expirado
    # pero el refresh token ya está en blacklist
    print("\n9️⃣ Intentando refrescar token en blacklist...")
    response = requests.post(f"{BASE_URL}/auth/refresh/", json={"refresh": refresh_token})
    print_response(response, "9. REFRESCAR TOKEN EN BLACKLIST")
    
    if response.status_code != 200:
        print("✅ Token correctamente en blacklist")
    else:
        print("❌ Token debería estar en blacklist")
    
    # 10. Intentar acceder sin token
    print("\n🔟 Intentando acceder sin token...")
    response = requests.get(f"{BASE_URL}/libros/")
    print_response(response, "10. ACCESO SIN TOKEN")
    
    if response.status_code == 401:
        print("✅ Correctamente bloqueado sin autenticación")
    else:
        print("❌ Debería requerir autenticación")
    
    print("\n" + "="*60)
    print("🎉 PRUEBAS COMPLETADAS")
    print("="*60)

if __name__ == "__main__":
    try:
        test_authentication()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se puede conectar al servidor")
        print("Asegúrate de que el servidor esté corriendo en http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
