from typing import List, Literal, TypedDict

class PathStep(TypedDict):
	kind: Literal["field", "index", "wildcard"]
	value: str | int | None

ParsedPath = List[PathStep]


def parse_path(expr: str | None) -> ParsedPath:
	if not expr:
		return []
	s = expr.strip()
	if s.startswith("$"):
		s = s[1:]
	# Accept leading dot like .a.b[0]
	steps: ParsedPath = []
	i = 0
	while i < len(s):
		c = s[i]
		if c == ".":
			i += 1
			start = i
			while i < len(s) and s[i] not in ".[":
				i += 1
			name = s[start:i]
			if not name:
				raise ValueError("Пустое имя поля в пути")
			steps.append({"kind": "field", "value": name})
			continue
		if c == "[":
			i += 1
			if i < len(s) and s[i] == "*":
				# wildcard index
				i += 1
				if i >= len(s) or s[i] != "]":
					raise ValueError("Ожидалась ']' после '*'")
				i += 1
				steps.append({"kind": "wildcard", "value": None})
				continue
			# numeric index
			start = i
			while i < len(s) and s[i].isdigit():
				i += 1
			if start == i:
				raise ValueError("Ожидался числовой индекс или '*'")
			if i >= len(s) or s[i] != "]":
				raise ValueError("Ожидалась ']' после индекса")
			idx = int(s[start:i])
			i += 1
			steps.append({"kind": "index", "value": idx})
			continue
		# support starting without dot for first field
		start = i
		while i < len(s) and s[i] not in ".[":
			i += 1
		name = s[start:i]
		if name:
			steps.append({"kind": "field", "value": name})
			continue
		raise ValueError(f"Неожиданный символ в пути: {c}")
	return steps
