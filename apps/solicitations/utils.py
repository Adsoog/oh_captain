import requests

def provider_name(ruc):
    url = f"https://api.apis.net.pe/v2/sunat/ruc?numero={ruc}"
    token = "apis-token-12335.66f3s7HjN6Nel8gcQOHo0le531JKyeMB"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            data = response.json()
            razon_social = data.get('razonSocial', 'No disponible')
            return razon_social
        else:
            razon_social = "No se encontro"
            return razon_social
    except Exception as e:
        print(f"Se produjo un error al consultar el RUC {ruc}: {e}")
        return 'No disponible'
