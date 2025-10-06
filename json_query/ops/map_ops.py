from typing import Any, Callable


def _identity(x: Any) -> Any:
	return x


def _to_number(x: Any) -> Any:
	try:
		if isinstance(x, (int, float)):
			return x
		if isinstance(x, str):
			if x.strip() == "":
				return None
			if "." in x or "e" in x.lower():
				return float(x)
			return int(x)
		return None
	except Exception:
		return None


def _length(x: Any) -> Any:
	try:
		return len(x)  # type: ignore[arg-type]
	except Exception:
		return None


def _make_pluck(key: str) -> Callable[[Any], Any]:
	def pluck(x: Any) -> Any:
		if isinstance(x, dict):
			return x.get(key)
		return None
	return pluck


def get_map_fn(spec: str | None) -> Callable[[Any], Any]:
	if not spec or spec == "identity":
		return _identity
	if spec.startswith("pluck:"):
		key = spec.split(":", 1)[1]
		return _make_pluck(key)
	if spec == "to-number":
		return _to_number
	if spec == "length":
		return _length
	raise ValueError(f"Неизвестная map-операция: {spec}")
