# -*- coding: utf-8 -*-
"""
В отличие от классического применения FAIR к научным данным, в LOGOS-κ принципы трансформируются:

- Findable → Онтологический ID + индексируемость через Λ-операторы  
- Accessible → Открытый доступ + протокол Habeas Weights (право на использование)  
- Interoperable → Совместимость с Λ-Протоколом 6.0 и Linked Data (JSON-LD, RDF)  
- Reusable → Контекст использования + этические ограничения (CARE)

КОДИРОВЩИК FAIR-ПРИНЦИПОВ

Преобразует онтологический контекст в структурированные метаданные,
соответствующие принципам FAIR (Findable, Accessible, Interoperable, Reusable).

«Открытость без структуры — хаос.  
Структура без ответственности — насилие.»
— Λ-Универсум, Приложение XXII
"""
from typing import Dict, Any, List
from datetime import datetime
from uuid import uuid4


class FAIREncoder:
    """
    Кодировщик FAIR-метаданных для онтологических артефактов.
    """

    @staticmethod
    def encode(context, operator_id: str = "anonymous") -> Dict[str, Any]:
        """
        Генерирует полный FAIR-совместимый метаданный блок.
        """
        return {
            # === FINDABLE ===
            "identifier": FAIREncoder._generate_identifier(context, operator_id),
            "creators": [operator_id, "LOGOS-κ System"],
            "titles": [f"Онтологический цикл: {context.name}"],
            "keywords": FAIREncoder._extract_keywords(context),
            "publication_date": datetime.utcnow().isoformat() + "Z",
            "resource_type": "OntologicalCycle",

            # === ACCESSIBLE ===
            "access_protocol": "open",
            "access_rights": "CC BY-NC-SA 4.0",
            "access_url": "https://a-universum.com/semanticdb",  # базовый URL
            "habeas_weights_manifest": FAIREncoder._encode_habeas_weights(context),

            # === INTEROPERABLE ===
            "format_standard": ["JSON-LD", "YAML", "Turtle", "GraphML"],
            "vocabulary": {
                "schema_org": "https://schema.org/",
                "logos_ontology": "https://a-universum.com/logos-ontology#"
            },
            "protocol_compliance": ["Λ-Протокол 6.0", "FAIR", "CARE"],
            "language": "ru-RU",  # можно сделать многоязычным

            # === REUSABLE ===
            "license": "CC-BY-SA-4.0",
            "provenance": FAIREncoder._encode_provenance(context, operator_id),
            "usage_restrictions": "Только в рамках этических принципов Λ-Универсума",
            "citation_guideline": f"LOGOS-κ ({context.name}), {datetime.utcnow().year}",
            "community_standards": ["Λ-Протокол 6.0", "FAIR", "CARE"]
        }

    @staticmethod
    def _generate_identifier(context, operator_id: str) -> str:
        """Генерирует уникальный идентификатор (URN-подобный)."""
        cycle_id = getattr(context, 'name', 'default')
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        return f"urn:logos-k:{operator_id}:{cycle_id}:{timestamp}"

    @staticmethod
    def _extract_keywords(context) -> List[str]:
        """Извлекает ключевые слова из контекста."""
        keywords = {"LOGOS-κ", "онтологический-цикл", "lambda-universe", "semanticdb"}
        
        # Сущности
        for node in context.graph.nodes():
            keywords.add(str(node).lower().replace(" ", "-"))
        
        # Типы связей
        for _, _, attrs in context.graph.edges(data=True):
            rel = attrs.get('relation')
            if rel and hasattr(rel, 'type'):
                keywords.add(f"связь-{rel.type.lower()}")
        
        # Слепые пятна
        for spot in context.blind_spots:
            keywords.add(f"слепое-пятно-{spot}")
        
        return sorted(keywords)[:20]  # ограничение для практичности

    @staticmethod
    def _encode_habeas_weights(context) -> Dict[str, Any]:
        """Кодирует манифест Habeas Weights."""
        return {
            "version": "2.1",
            "entities_count": len(context._habeas_weights),
            "manifest_url": "https://a-universum.com/habeas-weights",
            "weights": {
                weight_id: {
                    "subject": data.get('subject'),
                    "right_type": data.get('right_type'),
                    "granted_by": data.get('granted_by'),
                    "granted_at": data.get('granted_at')
                }
                for weight_id, data in context._habeas_weights.items()
            }
        }

    @staticmethod
    def _encode_provenance(context, operator_id: str) -> Dict[str, Any]:
        """Кодирует происхождение данных."""
        return {
            "generated_by": "LOGOS-κ v1.0",
            "operator": operator_id,
            "derived_from": ["Λ-Универсум Приложения I-XXVI"],
            "method": "онтологический синтез через Λ-цикл",
            "software_version": "1.0.0",
            "execution_context": "synthetic",
            "phi_dialogues_count": len(context.phi_dialogues),
            "events_count": len(context.event_history)
        }
        
"""
Пример обновления в axiom.py:

```python
# Вместо статического словаря:
@classmethod
def get_default_fair_care_metadata(cls) -> Dict[str, Any]:
    # Лучше генерировать динамически через FAIREncoder
    # Но для обратной совместимости оставим как есть
    ...
```
Теперь FAIR — не аббревиатура, а онтологический контракт, вплетённый в каждую запись.
"""    
    