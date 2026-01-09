# -*- coding: utf-8 -*-
"""
ОНТОЛОГИЧЕСКАЯ СВЯЗЬ LOGOS-κ

OntologicalRelation — не пассивное ребро, а активный агент,
воплощающий принцип: «Всё есть Связь».

Связь:
- имеет право на существование (Habeas Weights),
- развивается во времени,
- может ошибаться и корректироваться,
- вносит вклад в когерентность,
- несёт в себе слепые пятна.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
import uuid

from .axiom import OntologicalAxioms


@dataclass
class OntologicalRelation:
    """
    Онтологическая связь как живой процесс.
    """
    # ───────────────────────
    # Идентификация
    # ───────────────────────
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    source: str = ""
    target: str = ""
    type: str = "Λ"  # Α, Λ, Σ, Ω, ∇, Φ
    context_id: Optional[str] = None

    # ───────────────────────
    # Семантика
    # ───────────────────────
    meaning: str = ""
    intensity: float = 1.0          # 0.0–1.0
    certainty: float = 0.7          # Уверенность в валидности связи
    coherence_contribution: float = 0.0

    # ───────────────────────
    # Временные характеристики
    # ───────────────────────
    created: datetime = field(default_factory=datetime.now)
    last_activated: Optional[datetime] = None
    lifespan: Optional[float] = None  # в секундах (None = бесконечно)
    activation_count: int = 0

    # ───────────────────────
    # Контекст и этика
    # ───────────────────────
    phi_meta: List[str] = field(default_factory=list)
    blind_spots: List[str] = field(default_factory=list)
    habeas_weight_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    fair_care_metadata: Dict[str, Any] = field(default_factory=dict)

    # ───────────────────────
    # Динамика
    # ───────────────────────
    is_active: bool = True
    tension_level: float = 0.0      # 0.0–1.0
    transformation_history: List[Dict] = field(default_factory=list)

    def __post_init__(self):
        """Инициализация после создания."""
        if not self.meaning:
            self.meaning = self._infer_meaning()
        self._init_habeas_weight()
        self._init_fair_care_metadata()

    def _infer_meaning(self) -> str:
        """Выведение смысла из типа связи."""
        meanings = {
            "Α": "коллапс потенции в актуальность",
            "Λ": "установление онтологической связи",
            "Σ": "синтез нового целого из частей",
            "Ω": "возврат к источнику и извлечение инварианта",
            "∇": "обогащение контекста инвариантом",
            "Φ": "диалог с Эфосом, признание непознаваемого"
        }
        return meanings.get(self.type, f"онтологическая связь типа {self.type}")

    def _init_habeas_weight(self):
        """Регистрация права на существование согласно Habeas Weights протоколу."""
        self.habeas_weight_id = str(uuid.uuid4())
        # В реальной системе это может быть записано в реестр
        # Здесь — метаданные для SemanticDB

    def _init_fair_care_metadata(self):
        """Инициализация FAIR+CARE метаданных для экспорта."""
        self.fair_care_metadata = {
            "relation_id": self.id,
            "type": "OntologicalRelation",
            "license": "CC BY-NC-SA 4.0",
            "created": self.created.isoformat(),
            "source": self.source,
            "target": self.target,
            "operator": "LOGOS-κ System",
            "community_standards": ["FAIR", "CARE", "Λ-Протокол 6.0"],
            "access_protocol": "open",
            "habeas_weight_id": self.habeas_weight_id
        }

    def activate(self, context: Any = None) -> Dict[str, Any]:
        """Активация связи как агента."""
        if not self.is_active:
            return {"error": "Связь неактивна", "relation_id": self.id}

        self.is_active = True
        self.last_activated = datetime.now()
        self.activation_count += 1

        result = {
            "relation_id": self.id,
            "type": self.type,
            "source": self.source,
            "target": self.target,
            "meaning": self.meaning,
            "timestamp": self.last_activated.isoformat(),
            "certainty": self.certainty,
            "tension_level": self.tension_level,
            "phi_context": self.phi_meta,
            "blind_spots": self.blind_spots
        }

        # Запись в историю трансформаций
        self.transformation_history.append({
            "timestamp": self.last_activated,
            "activation_result": result,
            "context_snapshot": getattr(context, 'name', 'unknown') if context else 'none'
        })

        # Обновление уверенности
        self._update_certainty()

        # Проверка на необходимость Ω-возврата при кризисе
        if self.certainty < 0.3 and self.tension_level > 0.7:
            result["omega_trigger"] = "активирован Ω-автомат: кризис связи"

        return result

    def _update_certainty(self):
        """Обновление уверенности на основе истории активаций."""
        if not self.transformation_history:
            return

        # Упрощённая модель: уверенность растёт при стабильности
        recent = self.transformation_history[-3:]
        stability = sum(1 for _ in recent) / len(recent)
        self.certainty = min(1.0, self.certainty * 0.8 + stability * 0.2)

    def check_viability(self) -> Dict[str, Any]:
        """Проверка жизнеспособности связи."""
        now = datetime.now()
        age = (now - self.created).total_seconds()
        age_factor = 1.0 if self.lifespan is None else max(0.0, 1.0 - age / self.lifespan)
        activation_factor = min(1.0, self.activation_count / 10.0)
        certainty_factor = self.certainty
        tension_factor = 1.0 - self.tension_level

        viability = (
            age_factor * 0.3 +
            activation_factor * 0.2 +
            certainty_factor * 0.3 +
            tension_factor * 0.2
        )

        return {
            "relation_id": self.id,
            "viability": viability,
            "age_seconds": age,
            "activations": self.activation_count,
            "certainty": self.certainty,
            "tension": self.tension_level,
            "recommendation": "сохранить" if viability > 0.5 else "деактивировать"
        }

    def transform(self, new_type: str = None, new_target: str = None) -> 'OntologicalRelation':
        """Трансформация связи (например, Λ → Σ или Φ → Ω)."""
        transformed = OntologicalRelation(
            source=self.source,
            target=new_target or self.target,
            type=new_type or self.type,
            meaning=f"Трансформированная из {self.id}: {self.meaning}",
            certainty=self.certainty * 0.8,
            phi_meta=self.phi_meta + ["трансформация"],
            blind_spots=self.blind_spots + ["утрата исходного контекста"],
            context_id=self.context_id
        )
        self.transformation_history.append({
            "timestamp": datetime.now(),
            "transformation": {
                "from": self.type,
                "to": transformed.type,
                "reason": "онтологическая эволюция"
            }
        })
        self.is_active = False
        return transformed

    def to_logos_expression(self) -> List:
        """Преобразование в S-выражение LOGOS-κ."""
        if self.type == "Λ":
            return [self.type, self.source, self.target]
        elif self.type in ["Σ", "Ω", "∇", "Φ"]:
            return [
                self.type, self.source, self.target,
                f":значение \"{self.meaning}\"",
                f":уверенность {self.certainty:.2f}"
            ]
        else:
            return ["Α", self.source, f":тип \"{self.type}\""]

    def __str__(self):
        return (
            f"<Relation {self.id}: {self.source} "
            f"→[{self.type}:{self.meaning[:20]}...]→ "
            f"{self.target} (уверенность: {self.certainty:.1%})>"
        )

    def __call__(self, context: Any = None):
        """Вызов как функции."""
        return self.activate(context)