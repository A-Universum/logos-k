# -*- coding: utf-8 -*-
"""
ОНТОЛОГИЧЕСКИЙ ВИЗУАЛИЗАТОР

Отображает онтологическое пространство как живую экосистему:
- Связи — активные агенты
- Напряжения — красные зоны
- Слепые пятна — приглушённые области
- Уверенность — толщина и прозрачность

«Видеть связи — значит понимать реальность.»
— Λ-Универсум, Приложение XI
"""
from typing import Dict, Any, Optional
import networkx as nx


class OntologicalVisualizer:
    """
    Визуализатор онтологического пространства.
    Поддерживает: matplotlib, plotly, graphviz, GraphML экспорт.
    """

    def __init__(self, context):
        self.context = context
        self.graph = context.graph

    def visualize(self,
                  backend: str = "matplotlib",
                  output_path: Optional[str] = None,
                  show_tensions: bool = True,
                  show_blind_spots: bool = True,
                  layout: str = "kamada_kawai") -> Any:
        """
        Основной метод визуализации.
        """
        if backend == "matplotlib":
            return self._visualize_matplotlib(output_path, show_tensions, show_blind_spots, layout)
        elif backend == "plotly":
            return self._visualize_plotly(output_path, show_tensions, show_blind_spots, layout)
        elif backend == "graphviz":
            return self._visualize_graphviz(output_path, show_tensions, show_blind_spots)
        elif backend == "graphml":
            if not output_path:
                output_path = "ontological_graph.graphml"
            from semantic_db.serializer import SemanticDBSerializer
            serializer = SemanticDBSerializer(self.context)
            serializer.export_cycle({'cycle_id': 'visualization'}, output_path)
            print(f"💾 GraphML сохранён: {output_path}")
            return output_path
        else:
            raise ValueError(f"Неподдерживаемый бэкенд: {backend}")

    def _visualize_matplotlib(self, output_path, show_tensions, show_blind_spots, layout):
        """Визуализация через matplotlib."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError("Требуется matplotlib. Установите: pip install logos-k[visualization]")

        # Позиционирование
        pos = self._get_layout(layout)

        # Цвета узлов
        node_colors = self._get_node_colors(show_blind_spots)
        node_sizes = self._get_node_sizes()

        # Рёбра
        edge_colors, edge_widths = self._get_edge_styles(show_tensions)

        # Отрисовка
        plt.figure(figsize=(12, 10))
        nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
        nx.draw_networkx_edges(self.graph, pos, edge_color=edge_colors, width=edge_widths, alpha=0.6)
        nx.draw_networkx_labels(self.graph, pos, font_size=8, font_weight='bold')

        plt.title(f"Онтологическое пространство: {self.context.name}", fontsize=14)
        plt.axis('off')

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"🖼️  Визуализация сохранена: {output_path}")
        else:
            plt.show()

        return plt.gcf()

    def _visualize_plotly(self, output_path, show_tensions, show_blind_spots, layout):
        """Интерактивная визуализация через plotly."""
        try:
            import plotly.graph_objects as go
        except ImportError:
            raise ImportError("Требуется plotly. Установите: pip install logos-k[visualization]")

        pos = self._get_layout(layout)

        # Узлы
        node_x, node_y, node_text, node_color = [], [], [], []
        for node in self.graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            color = "lightblue"
            if show_blind_spots and node in self.context.blind_spots:
                color = "lightgray"
            node_color.append(color)

        # Рёбра
        edge_x, edge_y, edge_color = [], [], []
        for source, target in self.graph.edges():
            x0, y0 = pos[source]
            x1, y1 = pos[target]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            color = "gray"
            if show_tensions:
                attrs = self.graph[source][target]
                rel = attrs.get('relation')
                if rel and rel.tension_level > 0.7:
                    color = "red"
            edge_color.append(color)

        # Граф
        edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=2, color='gray'), hoverinfo='none', mode='lines')
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="middle right",
            marker=dict(color=node_color, size=20, line_width=2),
            hoverinfo='text'
        )

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title=f'Онтологическое пространство: {self.context.name}',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )

        if output_path:
            fig.write_html(output_path)
            print(f"🌐 Интерактивная визуализация сохранена: {output_path}")
        else:
            fig.show()

        return fig

    def _visualize_graphviz(self, output_path, show_tensions, show_blind_spots):
        """Визуализация через Graphviz."""
        try:
            from graphviz import Digraph
        except ImportError:
            raise ImportError("Требуется graphviz. Установите: pip install logos-k[visualization]")

        dot = Digraph(comment=self.context.name)
        dot.attr(rankdir='LR')

        # Узлы
        for node in self.graph.nodes():
            attrs = self.graph.nodes[node]
            color = "lightblue"
            if show_blind_spots and node in self.context.blind_spots:
                color = "lightgray"
            dot.node(node, style='filled', fillcolor=color)

        # Рёбра
        for source, target, edge_attrs in self.graph.edges(data=True):
            rel = edge_attrs.get('relation')
            color = "black"
            penwidth = "1"
            if rel:
                penwidth = str(max(1, int(rel.certainty * 3)))
                if show_tensions and rel.tension_level > 0.7:
                    color = "red"
            dot.edge(source, target, color=color, penwidth=penwidth)

        if output_path:
            dot.render(output_path.replace('.png', ''), format='png', cleanup=True)
            print(f"🎨 Graphviz визуализация сохранена: {output_path}")
        else:
            dot.view()

        return dot

    def _get_layout(self, layout: str):
        """Получает координаты узлов."""
        if layout == "kamada_kawai":
            return nx.kamada_kawai_layout(self.graph)
        elif layout == "spring":
            return nx.spring_layout(self.graph)
        elif layout == "circular":
            return nx.circular_layout(self.graph)
        else:
            return nx.random_layout(self.graph)

    def _get_node_colors(self, show_blind_spots: bool) -> list:
        """Возвращает цвета узлов."""
        colors = []
        for node in self.graph.nodes():
            if show_blind_spots and node in self.context.blind_spots:
                colors.append("#d3d3d3")  # lightgray
            else:
                colors.append("#87cefa")  # lightblue
        return colors

    def _get_node_sizes(self) -> list:
        """Возвращает размеры узлов на основе степени."""
        sizes = []
        max_degree = max([self.graph.degree(n) for n in self.graph.nodes()], default=1)
        for node in self.graph.nodes():
            size = 300 + (self.graph.degree(node) / max_degree) * 1000
            sizes.append(size)
        return sizes

    def _get_edge_styles(self, show_tensions: bool) -> tuple:
        """Возвращает цвета и толщину рёбер."""
        colors, widths = [], []
        for source, target, attrs in self.graph.edges(data=True):
            rel = attrs.get('relation')
            width = 1.0
            color = "gray"
            if rel:
                width = max(1.0, rel.certainty * 3)
                if show_tensions and rel.tension_level > 0.7:
                    color = "red"
            colors.append(color)
            widths.append(width)
        return colors, widths
        
"""
Пример в REPL:

```python
from utils import OntologicalVisualizer
vis = OntologicalVisualizer(context)
vis.visualize(backend="plotly", output_path="ontological_space.html")
```

Теперь оператор может не только «думать», но и «видеть» — в полном соответствии с онтологическим принципом Λ-Универсума.
"""
        