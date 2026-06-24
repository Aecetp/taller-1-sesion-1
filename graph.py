from langgraph.graph import StateGraph, END
from state import GraphState
from nodes.researcher import researcher_node
from nodes.reviewer import reviewer_node
from nodes.writer import writer_node

def check_reliability(state: GraphState):
    """
    Arista condicional que decide el siguiente paso tras la revisión.
    """
    score = state.get("reliability_score", 0)
    retries = state.get("revision_retries", 0)
    
    # TODO 2: Implementar la arista condicional.
    # - Si score >= 70: pasar a redactar ('writer').
    # - Si score < 70 y retries < 3: volver a investigar ('researcher').
    # - De lo contrario: abortar el flujo ('abort').
    pass

def create_graph():
    """
    Construye y compila el StateGraph conectando todos los nodos.
    """
    # TODO 3: Instanciar el StateGraph con nuestro Estado centralizado (GraphState)
    builder = None
    
    # TODO 4: Agregar los Nodos (researcher, reviewer, writer)
    
    # Nodo especial para marcar el estado como abortado
    def abort_node(state: GraphState):
        return {"is_aborted": True}
    # (También debemos agregar este nodo abort_node al grafo)
    
    # TODO 5: Configurar el punto de entrada y las aristas estáticas.
    # Pista: 
    # - Punto de entrada: "researcher"
    # - De "researcher" va a "reviewer"
    # - De "abort_node" va a "writer"
    # - De "writer" va a END
    
    # TODO 6: Configurar la arista condicional de salida para "reviewer" usando check_reliability.
    # Pista: Define los mapeos a "writer", "researcher" y "abort_node".
    
    # TODO 7: Compilar el grafo
    graph = None
    
    return graph
