from typing import Any, Iterable


def reduce_items(items: Iterable[Any], spec: str) -> Any:
	if spec == "count":
		cnt = 0
		for _ in items:
			cnt += 1
		return cnt
	if spec == "sum":
		total = 0.0
		for x in items:
			try:
				total += float(x) if x is not None else 0.0
			except Exception:
				continue
		# Возвращаем int, если целое
		return int(total) if total.is_integer() else total
	if spec == "max":
		it = iter(items)
		try:
			m = next(it)
		except StopIteration:
			return None
		for x in it:
			try:
				if x is not None and (m is None or x > m):
					m = x
			except Exception:
				continue
		return m
	if spec == "min":
		it = iter(items)
		try:
			m = next(it)
		except StopIteration:
			return None
		for x in it:
			try:
				if x is not None and (m is None or x < m):
					m = x
			except Exception:
				continue
		return m
	if spec == "first":
		for x in items:
			return x
		return None
	if spec == "last":
		last = None
		for x in items:
			last = x
		return last
	raise ValueError(f"Неизвестная reduce-операция: {spec}")
