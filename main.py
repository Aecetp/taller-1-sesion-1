from dotenv import load_dotenv
from graph import create_graph

# Cargar variables de entorno antes de importar cualquier cosa que use LLMs
load_dotenv()

def print_separator(title=""):
    print(f"\n{'='*50}")
    if title:
        print(f" {title} ".center(50, "="))
    print(f"{'='*50}")

def run_lab():
    print_separator("LABORATORIO: SISTEMA MULTIAGENTE LANGGRAPH")
    
    # 1. Instanciamos el grafo
    graph = create_graph()
    
    # Si el grafo aún no ha sido compilado en graph.py, evitamos el crash
    if not graph:
        print("⚠️ El grafo aún no está construido. Completa graph.py primero.")
        return
        
    # 2. Definimos el tema de entrada
    topic = input("\n📝 Ingresa un tema de investigación (ej. 'Agujeros negros' o 'Cura del cáncer de manera fácil'): ")
    if not topic.strip():
        topic = "Impacto de la Inteligencia Artificial en la Educación"
        print(f"Usando tema por defecto: {topic}")
    
    # Estado inicial
    initial_state = {
        "topic": topic,
        "sources": [],
        "research_notes": "",
        "reliability_score": 0,
        "revision_retries": 0,
        "final_draft": "",
        "is_aborted": False
    }
    
    print_separator("INICIANDO FLUJO DEL GRAFO")
    
    # TODO 8: Ejecutar el grafo en modo stream y recorrer el bucle
    # para mostrar en pantalla qué nodo se completa y qué datos de fiabilidad o fuentes se actualizan.
    
    print_separator("RESULTADO FINAL")
    
    # TODO 9: Imprimir el final_draft resultante del último nodo ejecutado (writer)
    print("Aún no se ha impreso el resultado. Completa el bucle de stream en main.py.")

if __name__ == "__main__":
    run_lab()
