from typing import Iterable, Any, List, Optional

from ..path.parser import parse_path
from ..path.matcher import iter_match_path
from ..ops.map_ops import get_map_fn
from ..ops.reduce_ops import reduce_items


def execute_query(items: Iterable[Any], path_expr: Optional[str], map_spec: Optional[str], reduce_spec: Optional[str]) -> Any:
	path = parse_path(path_expr) if path_expr else None
	map_fn = get_map_fn(map_spec)

	transformed: List[Any] = []
	for item in items:
		# Применяем путь (если задан): выдаёт последовательность совпадений
		if path is not None:
			for matched in iter_match_path(item, path):
				mapped = map_fn(matched)
				transformed.append(mapped)
		else:
			mapped = map_fn(item)
			transformed.append(mapped)

	# Если указан reduce — агрегируем, иначе возвращаем полный список результатов
	if reduce_spec:
		return reduce_items(transformed, reduce_spec)
	return transformed


