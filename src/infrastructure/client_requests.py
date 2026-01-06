import requests
import json
import sys 

def print_separator():
    print("\n" + "-" * 80 + "\n")


def print_assitant_response(response):
    
    print_separator()
    print("\n 🤖 Asistente: ", response)
    print_separator()
    

    if isinstance(response, dict):
        
        if "to_user" in response:
            print_assitant_response(response["to_user"])
            

def make_request(url, headers, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
        sys.exit(1)

def create_client():

    print("\n 👤 Creando nuevo cliente...\n")
    print_separator()

def show_menu():
    print("\n" + "=" * 40)
    print("      APP DE SEGUROS - MENÚ PRINCIPAL")
    print("=" * 40)
    print("📄 1. Consultar mis seguros")
    print("   Revisa el detalle de tus seguros vigentes\n")
    print("☎️  2. Reportar emergencia")
    print("   Conoce los números para reportar alguna emergencia\n")
    print("💲 3. Pagos")
    print("   Consulta cómo pagar, estado de tus pagos\n")
    print("🔍 4. Inspección de mi auto")
    print("   Coordina tu inspección vehicular\n")
    print("📝 5. Gestiones y Reclamos")
    print("   Ingresa o consulta el estado de tu requerimiento\n")
    print("🛒 6. Cotizar un seguro")
    print("   Explora los seguros disponibles y recibe asesoría\n")
    print("🤔 7. Consultas Banco")
    print("   Conoce los canales de atención del banco\n") 
    print("=" * 40)

def consult_insurance_policy():
    print("\n🔍 Consultando información de pólizas...\n")
    
    # Placeholder details - Replace with actual API endpoint and valid data
    url = "https://api.insurance-provider.com/v1/policies/consult" # PLACEHOLDER
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_ACCESS_TOKEN", # PLACEHOLDER
        "Accept": "application/json"
    }
    
    # Swagger-style payload
    payload = {
        "client_identification": "12345678", # PLACEHOLDER
        "request_type": "active_policies"
    }

    print(f"Request URL: {url}")
    print(f"Method: POST")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    # Uncomment the following line to actually make the request
    # response = make_request(url, headers, payload)
    
    # Simulating a response for demonstration purposes
    simulated_response = {
        "status": "success",
        "data": {
            "policies": [
                {"policy_number": "POL-998877", "type": "Auto", "status": "Active"},
                {"policy_number": "POL-112233", "type": "Life", "status": "Active"}
            ]
        }
    }
    print_assitant_response(simulated_response)


def report_emergency():
    print("\n☎️  Reportando emergencia...\n")
    
    # Placeholder details
    url = "https://api.insurance-provider.com/v1/emergencies/report"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_ACCESS_TOKEN", 
        "Accept": "application/json"
    }
    
    payload = {
        "client_identification": "12345678",
        "emergency_type": "Car Accident",
        "location": "Current GPS Location"
    }

    print(f"Request URL: {url}")
    print(f"Method: POST")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    # response = make_request(url, headers, payload)
    
    simulated_response = {
        "status": "success",
        "data": {
            "case_number": "EMG-2023-001",
            "message": "Emergencia reportada. Una unidad va en camino.",
            "estimated_arrival": "15 minutos"
        }
    }
    print_assitant_response(simulated_response)


def consult_payments():
    print("\n💲 Consultando pagos...\n")
    
    url = "https://api.insurance-provider.com/v1/payments/status"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Accept": "application/json"
    }
    
    payload = {
        "client_identification": "12345678"
    }

    print(f"Request URL: {url}")
    print(f"Method: GET") 
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    # response = make_request(url, headers, payload)

    simulated_response = {
        "status": "success",
        "data": {
            "outstanding_balance": 0.00,
            "last_payment_date": "2023-10-15",
            "next_payment_due": "2023-11-15",
            "amount_due": 150.00
        }
    }
    print_assitant_response(simulated_response)


def schedule_inspection():
    print("\n🔍 Coordinando inspección vehicular...\n")
    
    url = "https://api.insurance-provider.com/v1/inspections/schedule"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Accept": "application/json"
    }
    
    payload = {
        "client_identification": "12345678",
        "preferred_date": "2023-11-01",
        "plate_number": "ABC-123"
    }

    print(f"Request URL: {url}")
    print(f"Method: POST")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    # response = make_request(url, headers, payload)
    
    simulated_response = {
        "status": "success",
        "data": {
            "inspection_id": "INS-9988",
            "confirmed_date": "2023-11-01T10:00:00",
            "center": "Centro de Inspección Norte"
        }
    }
    print_assitant_response(simulated_response)


def manage_claims():
    print("\n📝 Gestionando reclamos...\n")
    
    url = "https://api.insurance-provider.com/v1/claims/list"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Accept": "application/json"
    }
    
    payload = {
        "client_identification": "12345678",
        "status_filter": "open"
    }

    print(f"Request URL: {url}")
    print(f"Method: POST")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    # response = make_request(url, headers, payload)
    
    simulated_response = {
        "status": "success",
        "data": {
            "claims": [
                {
                    "claim_id": "CLM-456",
                    "status": "In Review",
                    "description": "Minor bumper damage"
                }
            ]
        }
    }
    print_assitant_response(simulated_response)


def quote_new_insurance():
    print("\n🛒 Cotizando nuevo seguro...\n")
    
    url = "https://api.insurance-provider.com/v1/quotes/new"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Accept": "application/json"
    }
    
    payload = {
        "client_identification": "12345678",
        "insurance_type": "Home",
        "coverage_amount": 200000
    }

    print(f"Request URL: {url}")
    print(f"Method: POST")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    # response = make_request(url, headers, payload)
    
    simulated_response = {
        "status": "success",
        "data": {
            "quote_id": "QT-777",
            "monthly_premium": 25.50,
            "coverage_details": "Fire, Theft, Natural Disasters"
        }
    }
    print_assitant_response(simulated_response)


def consult_bank_channel():
    print("\n🤔 Consultando canales del banco...\n")
    
    url = "https://api.insurance-provider.com/v1/bank/channels"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Accept": "application/json"
    }
    
    payload = {
        "query": "customer service hours"
    }

    print(f"Request URL: {url}")
    print(f"Method: GET")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    # response = make_request(url, headers, payload)
    
    simulated_response = {
        "status": "success",
        "data": {
            "phone": "555-0199",
            "website": "www.bank.com",
            "hours": "Mon-Fri 9am-5pm"
        }
    }
    print_assitant_response(simulated_response)


def main():
    while True:
        show_menu()
        choice = input("\n👉 Selecciona una opción (1-7) o 'q' para salir: ")

        if choice == '1':
            consult_insurance_policy()
        elif choice == '2':
            report_emergency()
        elif choice == '3':
            consult_payments()
        elif choice == '4':
            schedule_inspection()
        elif choice == '5':
            manage_claims()
        elif choice == '6':
            quote_new_insurance()
        elif choice == '7':
            consult_bank_channel()
        elif choice.lower() == 'q':
            print("\n👋 Saliendo de la aplicación. ¡Hasta luego!\n")
            break
        else:
            print("\n❌ Opción no válida. Por favor intenta de nuevo.\n")
        
        input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()