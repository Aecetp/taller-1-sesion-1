from typing import Annotated, TypedDict, List
import operator

class GraphState(TypedDict):
    """
    Estado centralizado del flujo de trabajo.
    Todos los nodos leen y escriben en esta estructura.
    """
    # Tema de investigación ingresado por el usuario
    topic: str
    
    # TODO 1: Define una lista de fuentes 'sources' que ACUMULE las búsquedas en lugar de sobrescribirlas.
    # Pista: Usa Annotated y operator.add.
    
    # Resumen o notas de la investigación
    research_notes: str
    
    # Métrica de fiabilidad calculada por el revisor (0 a 100)
    reliability_score: int
    
    # Conteo de intentos de investigación y revisión (para evitar bucles infinitos)
    revision_retries: int
    
    # Borrador final redactado
    final_draft: str
    
    # Flag para indicar si la investigación fue abortada por baja calidad continua
    is_aborted: bool
