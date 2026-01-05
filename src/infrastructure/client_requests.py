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


def main():
    while True:
        show_menu()
        choice = input("\n👉 Selecciona una opción (1-7) o 'q' para salir: ")

        if choice == '1':
            consult_insurance_policy()
        elif choice == '2':
            print("\n☎️  Opción Reportar emergencia seleccionada (No implementada)\n")
        elif choice == '3':
            print("\n💲 Opción Pagos seleccionada (No implementada)\n")
        elif choice == '4':
            print("\n🔍 Opción Inspección de mi auto seleccionada (No implementada)\n")
        elif choice == '5':
            print("\n📝 Opción Gestiones y Reclamos seleccionada (No implementada)\n")
        elif choice == '6':
            print("\n🛒 Opción Cotizar un seguro seleccionada (No implementada)\n")
        elif choice == '7':
            print("\n🤔 Opción Consultas Banco seleccionada (No implementada)\n")
        elif choice.lower() == 'q':
            print("\n👋 Saliendo de la aplicación. ¡Hasta luego!\n")
            break
        else:
            print("\n❌ Opción no válida. Por favor intenta de nuevo.\n")
        
        input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()