# Guía del Instructor: Live Coding en 2 Horas (LangGraph Introducción)

Esta guía detalla la estrategia pedagógica para llevar a cabo el taller interactivo de 2 horas. Define qué archivos dejar preconstruidos, qué bloques de código vaciar con comentarios `TODO` para que los estudiantes los completen en vivo, y proporciona los bloques de "Antes" y "Después".

---

## 🗺️ Estrategia Pedagógica: ¿Qué se pre-construye y qué se codifica?

Para optimizar el tiempo de 2 horas y enfocarse en los fundamentos de LangGraph (Razonamiento distribuido, Estado, Nodos y Edges Condicionales):

1. **Pre-construido (Estático):**
   - La conexión al LLM (`utils/llm.py`) y el archivo `.env.example`.
   - Los System Prompts de los agentes. (Redactar prompts en vivo consume mucho tiempo y desvía la atención de LangGraph).
2. **Live-Coding (A completar por los alumnos):**
   - **`state.py`**: Definir el estado y aplicar el reductor de fuentes (`operator.add`).
   - **`nodes/*.py`**: Cómo cada nodo lee datos del `state`, cómo invoca al LLM y cómo retorna los campos actualizados.
   - **`graph.py`**: Conectar la lógica de nodos, aristas estáticas, arista condicional (`check_reliability`) y compilar.
   - **`main.py`**: Invocar el grafo mediante `graph.stream(...)` para visualizar el paso de estado en tiempo real.

---

## 📝 Bloques a Completar en Vivo (Paso a Paso)

### Paso 1: Configurar el Estado Centralizado (`state.py`)

**Concepto a explicar:**
- En LangGraph, el Estado es un diccionario estructurado (`TypedDict`) que se pasa entre nodos.
- Por defecto, los valores se sobrescriben. Para **acumular** datos (como las fuentes encontradas), usamos un *Reducer* (`Annotated` + `operator.add`).

#### ❌ Plantilla del Estudiante
```python
class GraphState(TypedDict):
    topic: str
    
    # TODO 1: Define una lista de fuentes 'sources' que ACUMULE las búsquedas en lugar de sobrescribirlas
    # Pista: Usa Annotated y operator.add
    
    research_notes: str
    reliability_score: int
    revision_retries: int
    final_draft: str
    is_aborted: bool
```

####   Solución
```python
    sources: Annotated[List[str], operator.add]
```

---

### Paso 2: Programación de Nodos / Agentes (`nodes/`)

**Concepto a explicar:**
- Un nodo en LangGraph es simplemente una función de Python que recibe el estado actual y devuelve un diccionario con las llaves que desea actualizar o agregar.

#### 🤖 Nodo Investigador (`nodes/researcher.py`)

##### ❌ Plantilla del Estudiante
```python
def researcher_node(state: GraphState):
    """
    Simula la búsqueda de fuentes de información y la generación de notas.
    """
    # TODO: 1. Recuperar el tema ('topic') del estado
    topic = ""
    
    # TODO: 2. Inicializar el LLM usando la función get_llm
    llm = None
    
    system_prompt = """Eres un investigador experto. Tu tarea es encontrar información detallada 
    sobre el tema proporcionado y listar al menos 4 fuentes (pueden ser URLs simuladas, libros o artículos) 
    relevantes de donde "obtuviste" la información."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Tema a investigar: {topic}")
    ]
    
    # TODO: 3. Invocar al LLM con los mensajes
    response = None
    
    # Mock de fuentes (estático)
    mock_sources = [
        f"https://ejemplo.com/articulo-1-{topic.replace(' ', '-')}",
        f"https://ejemplo.com/estudio-2-{topic.replace(' ', '-')}",
        "Libro: Fundamentos Avanzados",
        "Paper: Análisis de tendencias 2024"
    ]
    
    # TODO: 4. Retornar un diccionario con los campos que queremos actualizar en el Estado
    # (research_notes y sources)
    return {}
```

#####   Solución
```python
def researcher_node(state: GraphState):
    topic = state.get("topic", "")
    llm = get_llm()
    
    system_prompt = """Eres un investigador experto. Tu tarea es encontrar información detallada 
    sobre el tema proporcionado y listar al menos 4 fuentes (pueden ser URLs simuladas, libros o artículos) 
    relevantes de donde "obtuviste" la información."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Tema a investigar: {topic}")
    ]
    
    response = llm.invoke(messages)
    
    mock_sources = [
        f"https://ejemplo.com/articulo-1-{topic.replace(' ', '-')}",
        f"https://ejemplo.com/estudio-2-{topic.replace(' ', '-')}",
        "Libro: Fundamentos Avanzados",
        "Paper: Análisis de tendencias 2024"
    ]
    
    return {
        "research_notes": response.content,
        "sources": mock_sources
    }
```

---

#### 🔍 Nodo Revisor (`nodes/reviewer.py`)

##### ❌ Plantilla del Estudiante
```python
def reviewer_node(state: GraphState):
    """
    Audita las notas de la investigación y evalúa su fiabilidad para evitar alucinaciones.
    """
    # TODO: 1. Recuperar notas, fuentes y tema del estado
    notes = ""
    sources = []
    topic = ""
    
    # TODO: 2. Obtener el LLM con temperatura 0 para mayor consistencia
    llm = None
    
    system_prompt = f"""Eres un auditor estricto. Revisa las notas de investigación sobre '{topic}' 
    y verifica que se apoyen lógicamente en algo sólido. Evalúa la fiabilidad del 0 al 100.
    Sé muy crítico y meticuloso. Solo devuelve un número entero del 0 al 100 sin texto adicional."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Notas: {notes}\nFuentes citadas: {sources}")
    ]
    
    reliability = 0
    try:
        # TODO: 3. Invocar al LLM
        response = None
        
        # Lógica de extracción de número (estático para robustez)
        score_text = response.content.strip()
        import re
        match = re.search(r'\d+', score_text)
        reliability = int(match.group()) if match else random.randint(50, 90)
    except Exception:
        reliability = random.randint(50, 90)
        
    # TODO: 4. Incrementar el contador de revisiones
    current_retries = 0
    
    # TODO: 5. Retornar campos actualizados del estado (reliability_score y revision_retries)
    return {}
```

#####   Solución
```python
def reviewer_node(state: GraphState):
    notes = state.get("research_notes", "")
    sources = state.get("sources", [])
    topic = state.get("topic", "")
    
    llm = get_llm(temperature=0)
    
    system_prompt = f"""Eres un auditor estricto. Revisa las notas de investigación sobre '{topic}' 
    y verifica que se apoyen lógicamente en algo sólido. Evalúa la fiabilidad del 0 al 100.
    Sé muy crítico y meticuloso. Solo devuelve un número entero del 0 al 100 sin texto adicional."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Notas: {notes}\nFuentes citadas: {sources}")
    ]
    
    reliability = 0
    try:
        response = llm.invoke(messages)
        score_text = response.content.strip()
        import re
        match = re.search(r'\d+', score_text)
        reliability = int(match.group()) if match else random.randint(50, 90)
    except Exception:
        reliability = random.randint(50, 90)
        
    current_retries = state.get("revision_retries", 0) + 1
    
    return {
        "reliability_score": reliability,
        "revision_retries": current_retries
    }
```

---

#### ✍️ Nodo Redactor (`nodes/writer.py`)

##### ❌ Plantilla del Estudiante
```python
def writer_node(state: GraphState):
    """
    Formatea la investigación en un documento final si pasó la revisión.
    Si fue abortada por baja calidad, genera un reporte indicando la falla.
    """
    is_aborted = state.get("is_aborted", False)
    topic = state.get("topic", "")
    
    if is_aborted:
        # Lógica estática para el caso de abortar flujo
        draft = (f"**Reporte de Investigación Abortado**\n\n"
                 f"**Tema:** {topic}\n\n"
                 f"Tras múltiples intentos de investigación y revisión cruzada, "
                 f"el modelo concluye que no está preparado para dar información verídica...\n")
        return {"final_draft": draft}
        
    # TODO: 1. Obtener notas de investigación y fiabilidad del estado
    notes = ""
    score = 0
    
    # TODO: 2. Inicializar el LLM
    llm = None
    
    system_prompt = """Eres un redactor profesional experto en crear reportes formales listos para revisión humana (HITL).
    Toma las notas crudas de investigación y dales formato de artículo o reporte final.
    IMPORTANTE: Al final del documento, expón sutilmente la métrica de fiabilidad obtenida en la auditoría."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Notas a redactar: {notes}\nMétrica de fiabilidad de los datos: {score}/100")
    ]
    
    # TODO: 3. Invocar al LLM
    response = None
    
    # TODO: 4. Retornar el reporte final redactado ('final_draft')
    return {}
```

#####   Solución
```python
def writer_node(state: GraphState):
    is_aborted = state.get("is_aborted", False)
    topic = state.get("topic", "")
    
    if is_aborted:
        draft = (f"**Reporte de Investigación Abortado**\n\n"
                 f"**Tema:** {topic}\n\n"
                 f"Tras múltiples intentos de investigación y revisión cruzada, "
                 f"el modelo concluye que no está preparado para dar información verídica "
                 f"y 100% confiable sobre este tema aún.\n"
                 f"Se requiere intervención y revisión humana profunda antes de publicar resultados.")
        return {"final_draft": draft}
        
    notes = state.get("research_notes", "")
    score = state.get("reliability_score", 0)
    
    llm = get_llm()
    
    system_prompt = """Eres un redactor profesional experto en crear reportes formales listos para revisión humana (HITL).
    Toma las notas crudas de investigación y dales formato de artículo o reporte final.
    IMPORTANTE: Al final del documento, expón sutilmente la métrica de fiabilidad obtenida en la auditoría."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Notas a redactar: {notes}\nMétrica de fiabilidad de los datos: {score}/100")
    ]
    
    response = llm.invoke(messages)
    
    return {
        "final_draft": response.content
    }
```

---

### Paso 3: Orquestar el Grafo (`graph.py`)

#### ❌ Plantilla del Estudiante
*(Revisar `graph.py` en la raíz del proyecto).*

####   Solución
```python
def check_reliability(state: GraphState):
    score = state.get("reliability_score", 0)
    retries = state.get("revision_retries", 0)
    
    print(f"\n[Evaluación] Fiabilidad: {score}% | Intento: {retries}/3")
    
    if score >= 70:
        return "writer"
    elif retries < 3:
        return "researcher"
    else:
        return "abort"

def create_graph():
    builder = StateGraph(GraphState)
    
    builder.add_node("researcher", researcher_node)
    builder.add_node("reviewer", reviewer_node)
    builder.add_node("writer", writer_node)
    
    def abort_node(state: GraphState):
        return {"is_aborted": True}
    builder.add_node("abort_node", abort_node)
    
    builder.set_entry_point("researcher")
    builder.add_edge("researcher", "reviewer")
    builder.add_edge("abort_node", "writer")
    builder.add_edge("writer", END)
    
    builder.add_conditional_edges(
        "reviewer",
        check_reliability,
        {
            "writer": "writer",
            "researcher": "researcher",
            "abort": "abort_node"
        }
    )
    
    return builder.compile()
```

---

### Paso 4: Ejecución en Streaming (`main.py`)

#### ❌ Plantilla del Estudiante
*(Revisar `main.py` en la raíz del proyecto).*

####   Solución
```python
    final_output = None
    for output in graph.stream(initial_state):
        final_output = output
        for node_name, state_update in output.items():
            print(f"\n[Nodo Completado]: {node_name}")
            if "reliability_score" in state_update:
                print(f"  └─ Fiabilidad evaluada: {state_update['reliability_score']}%")
            if "sources" in state_update:
                print(f"  └─ Fuentes acumuladas: {len(state_update['sources'])}")

    print_separator("RESULTADO FINAL")
    
    final_draft = ""
    if final_output and "writer" in final_output:
        final_draft = final_output["writer"].get("final_draft", "")
        
    print(final_draft)
```

---

## ⏱️ Distribución de Tiempo sugerida para el Taller (2 Horas)

| Bloque | Duración | Actividad del Instructor | Actividad del Estudiante |
| :--- | :--- | :--- | :--- |
| **Intro Teórica** | 25 min | Explicar Fundamentos (Cuándo distribuir razonamiento) y Anatomía de LangGraph. | Atender, hacer preguntas iniciales. |
| **Setup & Explicación** | 15 min | Clonar repo, configurar `.env`, revisar estructura modular y agentes estáticos. | Configurar claves API locales/Codespaces. |
| **Paso 1: El Estado** | 15 min | Explicar el concepto de State, mutaciones y reducciones (`operator.add`). | Escribir la definición del estado en `state.py`. |
| **Paso 2: Nodos** | 25 min | Explicar cómo cada nodo interactúa leyendo/escribiendo del Estado común. | Codificar la lógica interna de los 3 nodos en `nodes/`. |
| **Paso 3: El Grafo** | 25 min | Explicar el Builder, nodos, edges normales y la arista condicional. | Codificar las conexiones y la lógica en `graph.py`. |
| **Paso 4: Streaming & QA**| 15 min | Explicar el bucle `graph.stream(...)` y debugear casos de reintento. | Escribir la ejecución del stream en `main.py` y probar. |
