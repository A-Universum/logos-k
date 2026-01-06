#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ИСПОЛНЯЕМЫЙ ТЕСТ Λ-ГЕНЕЗИСА

Демонстрирует программный запуск полного онтологического цикла
и верификацию его результатов через SemanticDB.

Использование:
    python examples/test_lambda_genesis.py

Этот скрипт:
- Загружает lambda_genesis.lk
- Выполняет цикл с оператором "тестировщик_онтологии"
- Экспортирует результат в semantic_db/
- Проверяет наличие ключевых артефактов
- Подтверждает соответствие Λ-Протоколу 6.0

«Верификация — не подтверждение истины, а проверка честности карты.»
— Λ-Универсум, Приложение XXII
"""

import os
import sys
from pathlib import Path

# Добавляем корень проекта в sys.path для импорта
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from interpreter.lexer import OntologicalLexer
from interpreter.parser import OntologicalParser
from interpreter.evaluator import SyntheticOntologicalEvaluator
from semantic_db.validator import SemanticDBValidator


def main():
    print("🧪 Запуск теста Λ-генезиса...")
    
    # 1. Загрузка программы
    program_path = ROOT / "examples" / "lambda_genesis.lk"
    with open(program_path, 'r', encoding='utf-8') as f:
        source = f.read()

    # 2. Лексический и синтаксический анализ
    lexer = OntologicalLexer(source)
    tokens = lexer.tokenize()
    parser = OntologicalParser(tokens, lexer)
    program = parser.parse()

    if not program:
        print("❌ Ошибка: не удалось распарсить lambda_genesis.lk")
        sys.exit(1)

    # 3. Инициализация вычислителя
    evaluator = SyntheticOntologicalEvaluator("тест_генезиса")
    evaluator.context.set_operator("тестировщик_онтологии")
    evaluator.context.enable_fair_care_validation()

    # 4. Выполнение программы
    print("🌀 Выполнение Λ-цикла...")
    results, cycle_data = evaluator.eval_program(
        program,
        operator_id="тестировщик_онтологии",
        fair_care=True
    )

    print(f"✅ Выполнено {len(results)} выражений.")

    # 5. Валидация перед экспортом
    print("🔍 Валидация онтологической целостности...")
    SemanticDBValidator.validate_cycle(cycle_data, evaluator.context)
    print("✅ Валидация пройдена.")

    # 6. Экспорт в SemanticDB
    export_dir = ROOT / "semantic_db"
    export_dir.mkdir(exist_ok=True)
    export_path = export_dir / f"тест_генезиса_{cycle_data['cycle_id']}.yaml"
    
    evaluator.semantic_db.export_cycle(cycle_data, str(export_path))
    print(f"💾 Экспорт завершён: {export_path}")

    # 7. Проверка ключевых артефактов
    print("🔍 Проверка ключевых артефактов...")
    context = evaluator.context

    # Должен быть создан синтез "диалог"
    assert "диалог" in context.graph, "❌ Сущность 'диалог' не создана"
    print("✅ Сущность 'диалог' найдена.")

    # Должен быть выполнен Ω-возврат
    omega_events = [e for e in context.event_history if e.gesture == 'Ω']
    assert omega_events, "❌ Ω-жест не выполнен"
    print("✅ Ω-жест выполнен.")

    # Должен быть Φ-диалог
    assert context.phi_dialogues, "❌ Φ-диалог отсутствует"
    print("✅ Φ-диалог зафиксирован.")

    # Должны быть признаны слепые пятна
    assert context.blind_spots, "❌ Слепые пятна не зарегистрированы"
    print("✅ Слепые пятна признаны.")

    # Когерентность должна быть в разумных пределах
    coherence = context._dynamic_coherence()
    assert 0.3 <= coherence <= 1.0, f"❌ Когерентность вне диапазона: {coherence}"
    print(f"✅ Когерентность в норме: {coherence:.2%}")

    print("\n🎉 Тест Λ-генезиса УСПЕШНО пройден!")
    print("Артефакт готов к верификации в SemanticDB.")


if __name__ == "__main__":
    main()