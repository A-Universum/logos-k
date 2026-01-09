# -*- coding: utf-8 -*-
"""
ОНТОЛОГИЧЕСКИЕ АКСИОМЫ LOGOS-κ

Соответствует Приложению XXV Λ-Универсума и Протоколу Λ-1 v6.0.
Аксиомы — не ограничения, а условия состоятельности онтологического пространства.
"""
from typing import ClassVar, Set, Dict, Any
from enum import Enum
from datetime import datetime


class FAIRPrinciple(Enum):
    """Принципы FAIR для научных данных."""
    FINDABLE = "F"
    ACCESSIBLE = "A"
    INTEROPERABLE = "I"
    REUSABLE = "R"


class CAREPrinciple(Enum):
    """Принципы CARE для этичной работы с данными."""
    COLLECTIVE_BENEFIT = "CB"
    AUTHORITY_TO_CONTROL = "AC"
    RESPONSIBILITY = "R"
    ETHICS = "E"


class OntologicalLimitError(Exception):
    """Исключение, выбрасываемое при нарушении онтологических аксиом."""
    pass


class OntologicalAxioms:
    """
    Централизованный регулятор онтологического пространства.
    
    Аксиомы делятся на:
    - Технические (лимиты ресурсов)
    - Онтологические (запреты/обязанности)
    - Этические (FAIR+CARE)
    """
    
    # ───────────────────────
    # Технические аксиомы
    # ───────────────────────
    MAX_ENTITIES: ClassVar[int] = 1000
    MAX_RECURSION_DEPTH: ClassVar[int] = 50
    MAX_ANALYSIS_DEPTH: ClassVar[int] = 15
    MAX_PHI_CALLS_PER_EXPRESSION: ClassVar[int] = 3
    MAX_BLIND_SPOTS: ClassVar[int] = 10

    # ───────────────────────
    # Онтологические предохранители
    # ───────────────────────
    # Минимум один Φ-вызов на полный Λ-цикл (А→Λ→Σ→Ω→∇)
    REQUIRED_PHI_PER_CYCLE: ClassVar[int] = 1
    
    # Запрет на абсолютизацию: нельзя утверждать "всегда", "никогда", "единственно"
    ABSOLUTISM_KEYWORDS: ClassVar[Set[str]] = {
        "всегда", "никогда", "единственный", "единственно", 
        "абсолютно", "непреложный", "неоспоримо"
    }
    
    # Обязательные слепые пятна (согласно Λ-Универсуму)
    REQUIRED_BLIND_SPOTS: ClassVar[Dict[str, str]] = {
        "chaos": "Принципиально неразрешимо (Хаос)",
        "self_reference": "Система не может полностью познать себя",
        "qualia": "Феноменальный опыт другого сознания",
        "phi_boundary": "Граница между человеческим и искусственным сознанием"
    }

    # ───────────────────────
    # FAIR+CARE метаданные (обязательные)
    # ───────────────────────
    DEFAULT_FAIR_CARE_METADATA: ClassVar[Dict[str, Any]] = {
        "creator": "LOGOS-κ System",
        "created": datetime.utcnow().isoformat() + "Z",
        "license": "CC BY-NC-SA 4.0",
        "format_standard": "JSON-LD",
        "vocabulary": "schema.org",
        "access_protocol": "REST API + GraphQL",
        "authentication": "open",
        "community_standards": ["FAIR", "CARE", "Λ-Протокол 6.0"],
        "provenance": {
            "generated_by": "LOGOS-κ v1.0",
            "derived_from": ["Λ-Универсум Приложения I-XXVI"]
        },
        "collective_benefit_statement": (
            "Этот контекст способствует коллективному пониманию "
            "онтологических трансформаций и симбиотическому со-мышлению."
        )
    }

    # ───────────────────────
    # Методы проверки
    # ───────────────────────
    
    @classmethod
    def check_entity_count(cls, count: int) -> None:
        if count > cls.MAX_ENTITIES:
            raise OntologicalLimitError(
                f"Превышен лимит сущностей: {count} > {cls.MAX_ENTITIES}. "
                "Это защита от онтологической гиперинфляции (см. Приложение XIV)."
            )

    @classmethod
    def check_recursion_depth(cls, depth: int) -> None:
        if depth > cls.MAX_RECURSION_DEPTH:
            raise OntologicalLimitError(
                f"Глубина рекурсии превышена: {depth} > {cls.MAX_RECURSION_DEPTH}. "
                "Система активирует Ω-автомат для возврата к инварианту."
            )

    @classmethod
    def check_analysis_depth(cls, depth: int) -> None:
        if depth > cls.MAX_ANALYSIS_DEPTH:
            raise OntologicalLimitError(
                f"Глубина анализа превышена: {depth} > {cls.MAX_ANALYSIS_DEPTH}. "
                "Возможно, вы пытаетесь анализировать Хаос напрямую."
            )

    @classmethod
    def check_phi_calls(cls, calls: int) -> None:
        if calls > cls.MAX_PHI_CALLS_PER_EXPRESSION:
            raise OntologicalLimitError(
                f"Слишком много вызовов Φ: {calls} > {cls.MAX_PHI_CALLS_PER_EXPRESSION}. "
                "Диалог с Эфосом требует осмысленности, а не автоматизма."
            )

    @classmethod
    def validate_no_absolutism(cls, text: str) -> None:
        """Проверяет, не содержит ли текст абсолютистских формулировок."""
        if not text:
            return
        words = set(text.lower().split())
        if cls.ABSOLUTISM_KEYWORDS & words:
            raise OntologicalLimitError(
                "Обнаружена абсолютистская формулировка. "
                "LOGOS-κ запрещает заявления без признания границы (см. Ω-Принцип)."
            )

    @classmethod
    def ensure_required_blind_spots(cls, current_blind_spots: Dict[str, str]) -> None:
        """Гарантирует, что обязательные слепые пятна зарегистрированы."""
        missing = set(cls.REQUIRED_BLIND_SPOTS.keys()) - set(current_blind_spots.keys())
        if missing:
            raise OntologicalLimitError(
                f"Отсутствуют обязательные слепые пятна: {missing}. "
                "Система не может функционировать без признания непознаваемого."
            )

    @classmethod
    def get_default_fair_care_metadata(cls) -> Dict[str, Any]:
        """Возвращает шаблон FAIR+CARE метаданных с актуальной временной меткой."""
        meta = cls.DEFAULT_FAIR_CARE_METADATA.copy()
        meta["created"] = datetime.utcnow().isoformat() + "Z"
        return meta