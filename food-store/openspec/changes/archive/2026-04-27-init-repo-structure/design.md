## Context

Food Store inicia como un proyecto modular con frontend y backend desacoplados, acompañados de documentación (`docs/`) y directorio de specs/changes para escalabilidad. El estado previo no contaba con un estándar OPSX explícito ni segmentación por dominios, lo que dificultaba la colaboración ordenada y el escalado.

## Goals / Non-Goals

**Goals:**
- Definir una estructura de carpetas estándar y modular
- Separar backend y frontend desde el inicio
- Incluir carpetas base para specs, changes y documentación
- Facilitar el onboarding de cualquier dev y la evolución del repo

**Non-Goals:**
- No incluye implementar ningún feature/producto
- No fija el stack tecnológico específico de frontend o backend

## Decisions

- Carpeta raíz `frontend/`: alojará SPA, webapp, etc (stack a definir en futuros changes)
- Carpeta raíz `backend/`: alojará la API, lógica de negocio, backend (stack a definir)
- Carpeta `docs/` y `openspec/` para documentación y specs según SDD/OPSX
- Estandarización inicial usando OPSX, aunque la estructura se armó previamente para dejar registro contractual de la arquitectura

## Risks / Trade-offs

- [Riesgo] Crónica vs. realidad del repo: Puede quedar desincronización si los cambios se documentan después de implementarlos → Mitigación: priorizar siempre la sincronización real entre specs y código.
- [Trade-off] No documenta el stack -> habilitamos flexibilidad pero exigirá decisiones explícitas en futuros changes.

## Migration Plan

N/A. Todo ya está creado, solo se formaliza la estructura en openspec.

## Open Questions

- ¿Conviene incluir carpeta scripts/ para tooling común?
- ¿Se estandarizarán los workflows en el backend y frontend desde el inicio o por change?