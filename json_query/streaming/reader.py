import sys
from typing import IO, Any, Iterator, Optional
import json
import ijson


def open_input_stream(path: Optional[str]) -> IO[str]:
	if path is None:
		return sys.stdin
	return open(path, "r", encoding="utf-8")


def iter_json_stream(stream: IO[str], is_ndjson: bool) -> Iterator[Any]:
	if is_ndjson:
		for line in stream:
			line = line.strip()
			if not line:
				continue
			yield json.loads(line)
		return
	# Пытаемся распознать как большой массив и читать по элементам
	# Если не массив — читаем один JSON-объект целиком и выдаём его
	pos = stream.tell() if stream is not sys.stdin and stream.seekable() else None
	try:
		# Используем ijson для потокового чтения массива корневого уровня
		for item in ijson.items(stream, "item"):
			yield item
		return
	except Exception:
		# Откатываем позицию и читаем целиком
		if pos is not None:
			stream.seek(pos)
		obj = json.load(stream)
		if isinstance(obj, list):
			for x in obj:
				yield x
		else:
			yield obj
