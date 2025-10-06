from typing import Any, Iterator, List

from .parser import ParsedPath


def iter_match_path(root: Any, path: ParsedPath) -> Iterator[Any]:
	"""Итерирует по значениям, соответствующим пути.

	Поддерживает шаги: field, index, wildcard (для массивов).
	"""
	frontier: List[Any] = [root]
	for step in path:
		next_frontier: List[Any] = []
		kind = step["kind"]
		if kind == "field":
			name = step["value"]
			for node in frontier:
				if isinstance(node, dict) and name in node:
					next_frontier.append(node[name])
		elif kind == "index":
			idx = step["value"]
			for node in frontier:
				if isinstance(node, list):
					if -len(node) <= idx < len(node):
						next_frontier.append(node[idx])
		elif kind == "wildcard":
			for node in frontier:
				if isinstance(node, list):
					next_frontier.extend(node)
		else:
			raise ValueError(f"Неизвестный шаг пути: {kind}")
		frontier = next_frontier
		if not frontier:
			break
	for node in frontier:
		yield node
