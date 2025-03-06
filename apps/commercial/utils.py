import requests
from django.db import transaction
from apps.commercial.models.client_models import Branch, Client

def client_obtain_and_create(ruc):
    """Query the SUNAT API, create a client and its branches."""
    url_full = f"https://api.apis.net.pe/v2/sunat/ruc/full?numero={ruc}"
    url_basic = f"https://api.apis.net.pe/v2/sunat/ruc?numero={ruc}"
    token = "apis-token-12335.66f3s7HjN6Nel8gcQOHo0le531JKyeMB"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    try:
        # Request data from both the full and basic URLs
        response_full = requests.get(url_full, headers=headers)
        response_full.encoding = 'utf-8'
        data_full = response_full.json() if response_full.status_code == 200 else {}

        response_basic = requests.get(url_basic, headers=headers)
        response_basic.encoding = 'utf-8'
        data_basic = response_basic.json() if response_basic.status_code == 200 else {}

        # Imprime las respuestas para depuración
        print("=== FULL DATA RESPONSE ===")
        print(data_full)
        print("=== BASIC DATA RESPONSE ===")
        print(data_basic)

        # Combinar datos para el cliente: data_full tiene prioridad
        data = {**data_basic, **data_full}

        # Campos del cliente usando la data combinada
        client_data = {
            'business_name': data.get('razonSocial', 'No disponible'),
            'tax_id': data.get('numeroDocumento', 'No disponible'),
            'address': data.get('direccion', 'No disponible'),
            'department': data.get('departamento', 'No disponible'),
            'province': data.get('provincia', 'No disponible'),
            'district': data.get('distrito', 'No disponible'),
            'economic_activity': data.get('actividadEconomica', 'No disponible'),
            'status': data.get('estado', 'No disponible'),
            'condition': data.get('condicion', 'No disponible'),
            'is_retention_agent': data.get('EsAgenteRetencion', False),
            "workers_number": data.get("numeroTrabajadores", "Not available"),
            "billing_type": data.get("tipoFacturacion", "Computerized"),
            "accounting_type": data.get("tipoContabilidad", "Computerized"),
            "foreign_trade": data.get("comercioExterior", "No Activity"),
            "company_type": data.get("tipo", "Limited Liability Company"),
        }

        # Crear el cliente y las sucursales en una transacción
        with transaction.atomic():
            client = Client.objects.create(**client_data)

            # Para las sucursales usamos los datos de 'localesAnexos' de data_basic
            locales_anexos = data_basic.get('localesAnexos', [])
            if isinstance(locales_anexos, list):
                for branch_data in locales_anexos:
                    Branch.objects.create(
                        client=client,
                        name=branch_data.get('direccion', 'Sucursal sin nombre'),
                        address=branch_data.get('direccion', ''),
                        department=branch_data.get('departamento', ''),
                        province=branch_data.get('provincia', ''),
                        district=branch_data.get('distrito', ''),
                        is_headquarters=False  # Ajusta según tu lógica
                    )
            else:
                print("No 'localesAnexos' found or it's not a list in data_basic.")

        return client
    except Exception as e:
        print(f"Error while obtaining and creating client with RUC {ruc}: {e}")
        return None

