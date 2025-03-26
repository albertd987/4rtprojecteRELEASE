import os
import requests
from datetime import datetime

def create_github_release():
    # Obtener token de GitHub desde variable de entorno
    github_token = "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"  # Sin espacios, comillas correctas
    if not github_token:
        print("Error: No se encontró el token de GitHub. Asegúrate de configurar GITHUB_TOKEN")
        return
    
    # Configurar detalles del repositorio
    owner = 'albertd987'  # Tu usuario de GitHub
    repo = '4RTPROJECTERELEASE'
    
    # Generar tag con fecha y hora actual
    tag_name = datetime.now().strftime("release-%Y%m%d-%H%M%S")
    
    # URL de la API de GitHub para crear releases
    url = f'https://api.github.com/repos/{owner}/{repo}/releases'
    
    # Configurar headers para la solicitud
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Datos para crear la release
    data = {
        'tag_name': tag_name,
        'target_commitish': 'main',
        'name': f'Automatic Release {tag_name}',
        'body': 'Release generada automáticamente por Jenkins',
        'draft': False,
        'prerelease': False
    }
    
    # Crear la release
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 201:
            release_data = response.json()
            upload_url = release_data['upload_url'].replace('{?name,label}', '')
            
            # Subir el ejecutable a la release
            executable_name = 'random_program'  # Nombre del ejecutable
            try:
                with open(executable_name, 'rb') as file:
                    upload_headers = {
                        'Authorization': f'token {github_token}',
                        'Content-Type': 'application/octet-stream'
                    }
                    upload_response = requests.post(
                        f'{upload_url}?name={executable_name}', 
                        headers=upload_headers, 
                        data=file
                    )
                
                if upload_response.status_code in [200, 201]:
                    print(f'Release {tag_name} creada y ejecutable subido exitosamente')
                else:
                    print(f'Error al subir el ejecutable. Código de estado: {upload_response.status_code}')
                    print(f'Respuesta: {upload_response.text}')
            
            except FileNotFoundError:
                print(f"Error: No se encontró el archivo ejecutable '{executable_name}'")
        else:
            print(f'Error al crear la release. Código de estado: {response.status_code}')
            print(f'Respuesta: {response.text}')
    
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")

if __name__ == '__main__':
    create_github_release()