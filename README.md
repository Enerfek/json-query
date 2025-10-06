json-query (jq-light)
=====================

CLI-утилита для выборки данных из JSON по пути, с поддержкой потоковой обработки (NDJSON и большие массивы через ijson), а также простых операций map/reduce.

Возможности
-----------
- Фильтры по пути: упрощённый синтаксис пути наподобие `.a.b[0]`, `.items[*].price`.
- Потоковая обработка: чтение из stdin, файлов, NDJSON, больших массивов JSON (через `ijson`).
- Map/Reduce: базовые операции для преобразований и агрегирования (map: identity, pluck:key, to-number, length; reduce: sum, count, max, min, first, last).

Установка
---------
```bash
pip install -r requirements.txt
```

Запуск
------
```bash
python -m json_query --help
```

Примеры
-------
- Простой выбор по пути из файла:
```bash
python -m json_query --input examples/sample.json --path ".items[*].price" --map to-number --reduce sum
```

- Чтение NDJSON из stdin и подсчёт количества записей:
```bash
type examples/sample.ndjson | python -m json_query --ndjson --reduce count
```

- Потоковая обработка большого массива в файле (авто через ijson):
```bash
python -m json_query --input examples/large_array.json --path ".[*].user.id" --reduce count
```

Архитектура
-----------
- `json_query/cli.py` — CLI и флаги
- `json_query/engine/` — связка пути, map/reduce, агрегация
- `json_query/path/` — парсер пути и сопоставитель
- `json_query/ops/` — операции map/reduce
- `json_query/streaming/` — потоковое чтение JSON/NDJSON/больших массивов
- `docs/` — документация использования
- `examples/` — примеры входных данных

Синтаксис пути (упрощённый)
---------------------------
- Точка для доступа к полям объекта: `.a.b`
- Квадратные скобки для индексов массива: `[0]`
- Поддержка `*` внутри скобок для перебора всех элементов массива: `[*]`
- Комбинирование: `.items[*].price`

Ограничения
-----------
- Это облегчённая версия jq: без фильтров-предикатов, без сложных выражений и конвейеров.
- Map поддерживает только предопределённые операции.

Структура проекта
-----------------
См. директории `json_query/`, `docs/`, `examples/`.

Лицензия
--------
MIT

# DAG Library - Библиотека для работы с направленными ациклическими графами

Мощная и гибкая библиотека Python для работы с направленными ациклическими графами (DAG), предоставляющая широкий набор алгоритмов и утилит для анализа, визуализации и управления графами.

## 🌟 Основные возможности

- **Топологическая сортировка** - множественные алгоритмы (Kahn, DFS, лексикографическая)
- **Поиск путей** - кратчайшие, длинные и все возможные пути
- **Сериализация** - поддержка JSON, Pickle, YAML, XML, CSV форматов
- **Валидация** - проверка корректности DAG и обнаружение циклов
- **Визуализация** - экспорт в DOT, Mermaid, GraphML форматы
- **Метрики** - комплексный анализ графов и вычисление центральности
- **Построители** - создание различных типов графов

## 📦 Установка

```bash
# Клонирование репозитория
git clone <repository-url>
cd dag-library

# Установка зависимостей
pip install -r requirements.txt

# Установка библиотеки в режиме разработки
pip install -e .
```

## 🚀 Быстрый старт

```python
from dag_lib import DAG, Node, Edge, TopologicalSort

# Создание графа
dag = DAG("Мой проект")

# Добавление узлов
dag.add_node(Node("start", "Начало"))
dag.add_node(Node("process", "Обработка"))
dag.add_node(Node("end", "Завершение"))

# Добавление связей
dag.add_edge(Edge("start", "process"))
dag.add_edge(Edge("process", "end"))

# Топологическая сортировка
order = TopologicalSort.kahn_algorithm(dag)
print(f"Порядок выполнения: {order}")
```

## 📚 Документация

### Основные компоненты

#### DAG (Directed Acyclic Graph)
Основной класс для работы с графами:

```python
from dag_lib import DAG, Node, Edge

dag = DAG("Название графа")

# Добавление узлов
node = Node("id", "данные", {"атрибут": "значение"})
dag.add_node(node)

# Добавление ребер
edge = Edge("источник", "цель", вес=1.0)
dag.add_edge(edge)

# Получение информации
print(f"Узлов: {len(dag.get_nodes())}")
print(f"Ребер: {len(dag.get_edges())}")
print(f"Корни: {dag.get_roots()}")
print(f"Листья: {dag.get_leaves()}")
```

#### Топологическая сортировка

```python
from dag_lib.algorithms import TopologicalSort

# Алгоритм Кана
order = TopologicalSort.kahn_algorithm(dag)

# DFS алгоритм
order = TopologicalSort.dfs_algorithm(dag)

# Лексикографическая сортировка
order = TopologicalSort.lexicographical_sort(dag)

# Все возможные сортировки
all_orders = TopologicalSort.get_all_topological_sorts(dag)

# Проверка корректности
is_valid = TopologicalSort.is_topological_order(dag, order)
```

#### Поиск путей

```python
from dag_lib.algorithms import PathFinder

# Поиск пути между узлами
path = PathFinder.find_path(dag, "start", "end")

# Все пути между узлами
all_paths = PathFinder.find_all_paths(dag, "start", "end")

# Кратчайшие пути от узла
shortest = PathFinder.find_shortest_paths(dag, "start")

# Самый длинный путь
longest_path, length = PathFinder.find_longest_path(dag, "start", "end")

# Достижимые узлы
reachable = PathFinder.find_reachable_nodes(dag, "start")
```

#### Сериализация

```python
from dag_lib.serialization import JSONSerializer, PickleSerializer

# JSON сериализация
json_serializer = JSONSerializer()
data = json_serializer.serialize(dag)
restored_dag = json_serializer.deserialize(data)

# Pickle сериализация
pickle_serializer = PickleSerializer()
data = pickle_serializer.serialize(dag)
restored_dag = pickle_serializer.deserialize(data)

# Работа с файлами
json_serializer.serialize_to_file(dag, "graph.json")
restored_dag = json_serializer.deserialize_from_file("graph.json")
```

#### Визуализация

```python
from dag_lib.utils import GraphVisualizer

# DOT формат для Graphviz
dot_format = GraphVisualizer.to_dot_format(dag)

# Mermaid формат
mermaid_format = GraphVisualizer.to_mermaid_format(dag)

# Список смежности
adjacency_list = GraphVisualizer.to_adjacency_list(dag)

# Экспорт в файл
GraphVisualizer.export_to_file(dag, "graph.dot", "dot")
```

#### Построители графов

```python
from dag_lib.utils import GraphBuilder

# Линейный граф
linear_dag = GraphBuilder.create_linear_graph(5)

# Древовидный граф
tree_dag = GraphBuilder.create_tree_graph(height=3, branching_factor=2)

# Случайный DAG
random_dag = GraphBuilder.create_random_dag(n=100, edge_probability=0.3)

# DAG из зависимостей
dependencies = {
    "task_a": [],
    "task_b": ["task_a"],
    "task_c": ["task_a", "task_b"]
}
dag = GraphBuilder.create_dag_from_dependencies(dependencies)

# Многослойный DAG
layered_dag = GraphBuilder.create_layered_dag([2, 3, 2, 1])
```

#### Анализ и метрики

```python
from dag_lib.algorithms import GraphMetrics

# Базовые метрики
metrics = GraphMetrics.get_basic_metrics(dag)

# Статистика степеней
degree_stats = GraphMetrics.get_degree_statistics(dag)

# Меры центральности
centrality = GraphMetrics.get_centrality_measures(dag)

# Полный анализ
analysis = GraphMetrics.get_comprehensive_analysis(dag)
```

#### Валидация

```python
from dag_lib.utils import GraphValidator

# Валидация DAG
is_valid, errors = GraphValidator.validate_dag(dag)

# Валидация структуры
is_valid_structure, warnings = GraphValidator.validate_graph_structure(dag)

# Полный отчет
report = GraphValidator.get_validation_report(dag)

# Валидация для конкретного алгоритма
is_valid_for_algo, errors = GraphValidator.validate_for_algorithm(dag, "topological_sort")
```

## 📁 Структура проекта

```
dag-library/
├── src/
│   └── dag_lib/
│       ├── __init__.py
│       ├── core/                 # Основные компоненты
│       │   ├── graph.py         # Класс DAG
│       │   ├── node.py          # Класс Node
│       │   └── edge.py          # Класс Edge
│       ├── algorithms/          # Алгоритмы
│       │   ├── topological_sort.py
│       │   ├── pathfinding.py
│       │   ├── cycle_detection.py
│       │   └── graph_metrics.py
│       ├── serialization/       # Сериализация
│       │   ├── serializers.py
│       │   └── formats.py
│       ├── utils/               # Утилиты
│       │   ├── validators.py
│       │   ├── visualizers.py
│       │   ├── builders.py
│       │   └── exporters.py
│       └── exceptions.py        # Исключения
├── tests/                       # Тесты
│   ├── test_core.py
│   ├── test_algorithms.py
│   ├── test_serialization.py
│   └── test_utils.py
├── examples/                    # Примеры
│   ├── basic_usage.py
│   ├── advanced_examples.py
│   └── performance_examples.py
├── requirements.txt
└── README.md
```

## 🧪 Тестирование

```bash
# Запуск всех тестов
python -m pytest tests/

# Запуск с покрытием кода
python -m pytest tests/ --cov=src/dag_lib

# Запуск конкретного теста
python -m pytest tests/test_core.py

# Запуск примеров
python examples/basic_usage.py
python examples/advanced_examples.py
python examples/performance_examples.py
```

## 📊 Примеры использования

### Управление проектами

```python
from dag_lib import DAG, Node, Edge
from dag_lib.utils import GraphBuilder
from dag_lib.algorithms import TopologicalSort, PathFinder

# Создание графа проекта
dependencies = {
    "планирование": [],
    "дизайн": ["планирование"],
    "разработка": ["дизайн"],
    "тестирование": ["разработка"],
    "развертывание": ["тестирование"]
}

project_dag = GraphBuilder.create_dag_from_dependencies(dependencies)

# Планирование выполнения
execution_order = TopologicalSort.kahn_algorithm(project_dag)
print(f"Порядок выполнения: {execution_order}")

# Поиск критического пути
critical_path, duration = PathFinder.find_longest_path(
    project_dag, "планирование", "развертывание"
)
print(f"Критический путь: {critical_path}")
```

### Конвейер обработки данных

```python
from dag_lib.utils import GraphBuilder
from dag_lib.algorithms import GraphMetrics

# Создание многослойного конвейера
layers = [1, 3, 2, 1]  # источник -> обработка -> анализ -> вывод
pipeline = GraphBuilder.create_layered_dag(layers, "Конвейер данных")

# Анализ производительности
metrics = GraphMetrics.get_basic_metrics(pipeline)
print(f"Плотность конвейера: {metrics['density']:.3f}")

# Поиск узких мест
for node in pipeline.get_nodes():
    in_degree = pipeline.get_in_degree(node.id)
    if in_degree > 2:
        print(f"Узкое место: {node.id} (входящая степень: {in_degree})")
```

### Машинное обучение

```python
from dag_lib.utils import GraphBuilder

# ML конвейер
ml_workflow = {
    "сбор_данных": {"duration": 2, "dependencies": []},
    "предобработка": {"duration": 3, "dependencies": ["сбор_данных"]},
    "обучение": {"duration": 8, "dependencies": ["предобработка"]},
    "валидация": {"duration": 2, "dependencies": ["обучение"]},
    "развертывание": {"duration": 1, "dependencies": ["валидация"]}
}

ml_dag = GraphBuilder.create_workflow_graph(ml_workflow)

# Анализ времени выполнения
total_time = sum(task["duration"] for task in ml_workflow.values())
print(f"Общее время выполнения: {total_time} дней")
```

## 🔧 Расширение функциональности

### Создание пользовательского сериализатора

```python
from dag_lib.serialization.serializers import TextSerializer

class CustomSerializer(TextSerializer):
    def _text_serialize(self, data):
        # Ваша логика сериализации
        return custom_format_string
    
    def _text_deserialize(self, text):
        # Ваша логика десериализации
        return parsed_data
```

### Создание пользовательского построителя

```python
from dag_lib.utils.builders import GraphBuilder

def create_custom_graph(parameters):
    dag = DAG("Custom Graph")
    
    # Ваша логика создания графа
    for i in range(parameters['nodes']):
        node = Node(f"custom_{i}", f"Custom node {i}")
        dag.add_node(node)
    
    # Добавление ребер по вашей логике
    # ...
    
    return dag
```

## 📈 Производительность

Библиотека оптимизирована для работы с графами различного размера:

- **Малые графы** (< 100 узлов): мгновенная обработка
- **Средние графы** (100-1000 узлов): быстрая обработка
- **Большие графы** (1000+ узлов): эффективная обработка

Примеры производительности доступны в `examples/performance_examples.py`.

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие библиотеки! Пожалуйста:

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 🆘 Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте документацию и примеры
2. Поищите в Issues существующие решения
3. Создайте новый Issue с подробным описанием проблемы

## 🔮 Планы развития

- [ ] Поддержка параллельной обработки
- [ ] Интеграция с NetworkX
- [ ] Веб-интерфейс для визуализации
- [ ] Поддержка динамических графов
- [ ] Оптимизация памяти для больших графов
- [ ] Поддержка графов с временными метками

---

**DAG Library** - мощный инструмент для работы с направленными ациклическими графами в Python! 🚀