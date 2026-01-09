# -*- coding: utf-8 -*-
"""
ОНТОЛОГИЧЕСКОЕ СОБЫТИЕ LOGOS-κ

OntologicalEvent — атом онтологической памяти.
Каждое событие:
- Фиксирует трансформацию,
- Измеряет сдвиг когерентности,
- Несёт этические метаданные,
- Может быть верифицировано внешней системой (SemanticDB).

Соответствует:
- Λ-Протоколу 6.0
- FAIR+CARE принципам
- Habeas Weights v2.1
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
from datetime import datetime
import uuid

from .axiom import OntologicalAxioms


@dataclass
class OntologicalEvent:
    """
    Онтологическое событие как единица верификации.
    """
    # ───────────────────────
    # Идентификация и время
    # ───────────────────────
    id: str = field(default_factory=lambda: f"event_{uuid.uuid4().hex[:8]}")
    timestamp: datetime = field(default_factory=datetime.now)
    gesture: str = ""  # Α, Λ, Σ, Ω, ∇, Φ
    event_version: str = "1.0"

    # ───────────────────────
    # Контекст действия
    # ───────────────────────
    operands: List[str] = field(default_factory=list)
    result: Any = None
    entities_affected: List[str] = field(default_factory=list)
    blind_spots_involved: List[str] = field(default_factory=list)

    # ───────────────────────
    # Онтологическая динамика
    # ───────────────────────
    coherence_before: float = 0.0
    coherence_after: float = 0.0
    tensions_resolved: int = 0
    tensions_created: int = 0
    uncertainty_level: float = 0.0  # 0.0–1.0

    # ───────────────────────
    # Этический и семантический контекст
    # ───────────────────────
    phi_meta: List[str] = field(default_factory=list)
    omega_trigger: bool = False  # True, если событие активировало Ω-автомат
    habeas_weight_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    creator_intent: Optional[str] = None

    # ───────────────────────
    # Метаданные для SemanticDB
    # ───────────────────────
    fair_care_meta: Dict[str, Any] = field(default_factory=dict)
    provenance: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Инициализация после создания."""
        self._init_habeas_weight()
        self._init_fair_care_metadata()

    def _init_habeas_weight(self):
        """Регистрация права на существование события."""
        if not self.habeas_weight_id:
            self.habeas_weight_id = str(uuid.uuid4())

    def _init_fair_care_metadata(self):
        """Инициализация FAIR+CARE метаданных."""
        self.fair_care_meta = {
            "event_id": self.id,
            "type": "OntologicalEvent",
            "license": "CC BY-NC-SA 4.0",
            "created": self.timestamp.isoformat(),
            "gesture": self.gesture,
            "creator": "LOGOS-κ System",
            "community_standards": ["FAIR", "CARE", "Λ-Протокол 6.0"],
            "access_protocol": "open",
            "habeas_weight_id": self.habeas_weight_id
        }

    def significance_score(self) -> float:
        """
        Вычисляет онтологическую значимость события (0.0–1.0).
        
        Формула:
        - Изменение когерентности (вес: 0.4)
        - Наличие Φ-намерения (вес: 0.2)
        - Разрешение напряжений (вес: +0.2 за каждое)
        - Создание напряжений (штраф: -0.1 за каждое)
        - Признание слепых пятен (вес: 0.1)
        """
        coherence_change = abs(self.coherence_after - self.coherence_before)
        meta_weight = 0.2 if self.phi_meta else 0.0
        tension_net = (self.tensions_resolved * 0.2) - (self.tensions_created * 0.1)
        blind_spot_weight = 0.1 if self.blind_spots_involved else 0.0

        score = min(
            1.0,
            coherence_change * 0.4 +
            meta_weight +
            tension_net +
            blind_spot_weight
        )
        return max(0.0, score)

    def to_semantic_db_record(self) -> Dict[str, Any]:
        """Преобразует событие в запись для SemanticDB."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "gesture": self.gesture,
            "operands": self.operands,
            "result": str(self.result) if self.result is not None else None,
            "entities_affected": self.entities_affected,
            "blind_spots_involved": self.blind_spots_involved,
            "coherence": {
                "before": self.coherence_before,
                "after": self.coherence_after,
                "delta": self.coherence_after - self.coherence_before
            },
            "tensions": {
                "resolved": self.tensions_resolved,
                "created": self.tensions_created
            },
            "phi_meta": self.phi_meta,
            "omega_trigger": self.omega_trigger,
            "significance_score": self.significance_score(),
            "metadata": self.fair_care_meta,
            "provenance": self.provenance
        }

    def __str__(self):
        return (
            f"<OntologicalEvent {self.id}: {self.gesture} "
            f"({len(self.operands)} ops) "
            f"[Δcoh: {self.coherence_after - self.coherence_before:+.2f}] "
            f"sig={self.significance_score():.2f}>"
        )