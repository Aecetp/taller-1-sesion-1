from langchain_core.messages import SystemMessage, HumanMessage
from state import GraphState
from utils.llm import get_llm

def researcher_node(state: GraphState):
    """
    Simula la búsqueda de fuentes de información y la generación de notas.
    """
    # TODO 1: Recuperar el tema ('topic') del estado.
    topic = ""
    
    # TODO 2: Inicializar el LLM llamando a get_llm().
    llm = None
    
    system_prompt = """Eres un investigador experto. Tu tarea es encontrar información detallada 
    sobre el tema proporcionado y listar al menos 4 fuentes (pueden ser URLs simuladas, libros o artículos) 
    relevantes de donde "obtuviste" la información. 
    Devuelve un breve resumen de tu investigación."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Tema a investigar: {topic}")
    ]
    
    # TODO 3: Invocar al LLM con los mensajes construidos.
    response = None
    
    # Mock de fuentes de investigación (estático)
    mock_sources = [
        f"https://ejemplo.com/articulo-1-{topic.replace(' ', '-')}",
        f"https://ejemplo.com/estudio-2-{topic.replace(' ', '-')}",
        "Libro: Fundamentos Avanzados",
        "Paper: Análisis de tendencias 2024"
    ]
    
    # TODO 4: Retornar los campos actualizados en el estado: 'research_notes' y 'sources'.
    return {}
