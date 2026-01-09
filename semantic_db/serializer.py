# -*- coding: utf-8 -*-
"""
СЕРИАЛИЗАТОР SEMANTICDB LOGOS-κ

Преобразует онтологический контекст и циклы в машиночитаемые артефакты,
совместимые с Λ-Протоколом 6.0 и принципами FAIR+CARE.

Поддерживаемые форматы:
- YAML (человеко-читаемый отчёт)
- JSON-LD (семантическая совместимость)
- Turtle (RDF/OWL)
- GraphML (графовые базы)

Каждая запись — верифицируемый онтологический акт.
"""
import json
import yaml
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from core.context import EnhancedActiveContext
from core.axiom import OntologicalAxioms


class SemanticDBSerializer:
    """
    Сериализатор онтологических экспериментов в форматы SemanticDB.
    """

    def __init__(self, context: EnhancedActiveContext):
        self.context = context

    def export_cycle(self, cycle_data: Dict[str, Any], output_path: str):
        """
        Экспортирует полный онтологический цикл в указанный файл.
        Формат определяется расширением: .yaml, .json, .jsonld, .ttl, .graphml
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.suffix in ('.yaml', '.yml'):
            content = self.to_yaml(cycle_data)
            path.write_text(content, encoding='utf-8')
        elif path.suffix in ('.json', '.jsonld'):
            content = self.to_json_ld(cycle_data)
            path.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding='utf-8')
        elif path.suffix == '.ttl':
            content = self.to_turtle(cycle_data)
            path.write_text(content, encoding='utf-8')
        elif path.suffix == '.graphml':
            content = self.to_graphml(cycle_data)
            path.write_text(content, encoding='utf-8')
        else:
            # По умолчанию — YAML
            content = self.to_yaml(cycle_data)
            path.with_suffix('.yaml').write_text(content, encoding='utf-8')

    def to_yaml(self, cycle_data: Dict[str, Any]) -> str:
        """Генерирует человеко-читаемый YAML-отчёт."""
        report = {
            'metadata': {
                'type': 'OntologicalCycle',
                'version': '1.0',
                'protocol': 'Λ-Протокол 6.0',
                'created_at': datetime.now().isoformat(),
                'creator': self.context._operator_id or 'anonymous_operator',
                'license': 'CC BY-NC-SA 4.0',
                'fair_care': OntologicalAxioms.get_default_fair_care_metadata()
            },
            'cycle_summary': {
                'cycle_id': cycle_data['cycle_id'],
                'timestamp': cycle_data['timestamp'],
                'expressions_evaluated': cycle_data['expressions_evaluated'],
                'successful_evaluations': cycle_of_data.get('successful_evaluations', 0),
                'final_coherence': cycle_data['final_coherence'],
                'phi_dialogues_count': cycle_data['phi_dialogues_count'],
                'nigc_scores': cycle_data.get('nigc_scores', [])
            },
            'ontological_context': {
                'entities': self._serialize_entities(),
                'relations': self._serialize_relations(),
                'blind_spots': self.context.blind_spots,
                'tensions': self.context.tension_log,
                'habeas_weights': self.context._habeas_weights
            },
            'event_history': [
                event.to_semantic_db_record()
                for event in self.context.event_history
            ],
            'phi_dialogues': self.context.phi_dialogues
        }
        return yaml.dump(report, allow_unicode=True, default_flow_style=False, indent=2)

    def to_json_ld(self, cycle_data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует JSON-LD документ для семантической совместимости."""
        return {
            "@context": {
                "schema": "https://schema.org/",
                "logos": "https://a-universum.com/logos-ontology#",
                "cycle": "logos:OntologicalCycle",
                "event": "logos:OntologicalEvent",
                "phiDialog": "logos:PhiDialogue"
            },
            "@type": "logos:OntologicalCycle",
            "logos:cycleId": cycle_data['cycle_id'],
            "schema:dateCreated": cycle_data['timestamp'],
            "logos:operator": self.context._operator_id or "anonymous",
            "logos:finalCoherence": cycle_data['final_coherence'],
            "logos:events": [
                event.to_semantic_db_record()
                for event in self.context.event_history
            ],
            "logos:phiDialogues": self.context.phi_dialogues,
            "logos:blindSpots": list(self.context.blind_spots.keys())
        }

    def to_turtle(self, cycle_data: Dict[str, Any]) -> str:
        """Генерирует Turtle (RDF) представление."""
        lines = [
            "@prefix logos: <https://a-universum.com/logos-ontology#> .",
            "@prefix schema: <https://schema.org/> .",
            "",
            f"<urn:cycle:{cycle_data['cycle_id']}>",
            "  a logos:OntologicalCycle ;",
            f"  schema:dateCreated \"{cycle_data['timestamp']}\"^^schema:DateTime ;",
            f"  logos:operator \"{self.context._operator_id or 'anonymous'}\" ;",
            f"  logos:finalCoherence {cycle_data['final_coherence']} ;",
            f"  logos:hasBlindSpot {' , '.join(f'\"{spot}\"' for spot in self.context.blind_spots.keys())} ;",
            "  ."
        ]
        return "\n".join(lines)

    def to_graphml(self, cycle_data: Dict[str, Any]) -> str:
        """Генерирует GraphML представление онтологического графа."""
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
            '  <key id="label" for="all" attr.name="label" attr.type="string"/>',
            '  <key id="type" for="node" attr.name="type" attr.type="string"/>',
            '  <key id="certainty" for="edge" attr.name="certainty" attr.type="double"/>',
            '  <graph id="ontological_context" edgedefault="directed">'
        ]

        # Узлы
        for node, attrs in self.context.graph.nodes(data=True):
            node_type = attrs.get('type', 'entity')
            lines.append(f'    <node id="{node}">')
            lines.append(f'      <data key="label">{node}</data>')
            lines.append(f'      <data key="type">{node_type}</data>')
            lines.append('    </node>')

        # Рёбра
        for source, target, edge_attrs in self.context.graph.edges(data=True):
            relation = edge_attrs.get('relation')
            certainty = relation.certainty if relation else 1.0
            edge_id = f"{source}_{target}"
            lines.append(f'    <edge id="{edge_id}" source="{source}" target="{target}">')
            lines.append(f'      <data key="certainty">{certainty}</data>')
            lines.append('    </edge>')

        lines.extend([
            '  </graph>',
            '</graphml>'
        ])
        return "\n".join(lines)

    def _serialize_entities(self) -> List[Dict[str, Any]]:
        """Сериализует все сущности контекста."""
        return [
            {
                'name': node,
                'attributes': dict(attrs)
            }
            for node, attrs in self.context.graph.nodes(data=True)
        ]

    def _serialize_relations(self) -> List[Dict[str, Any]]:
        """Сериализует все связи как активных агентов."""
        relations = []
        for source, target, edge_attrs in self.context.graph.edges(data=True):
            relation = edge_attrs.get('relation')
            if relation:
                relations.append({
                    'source': source,
                    'target': target,
                    'relation': {
                        'id': relation.id,
                        'type': relation.type,
                        'meaning': relation.meaning,
                        'certainty': relation.certainty,
                        'tension_level': relation.tension_level,
                        'habeas_weight_id': relation.habeas_weight_id,
                        'fair_care_metadata': relation.fair_care_metadata
                    }
                })
        return relations