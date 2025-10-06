import sys
import json
import click
from typing import Optional

from .engine.query import execute_query
from .streaming.reader import open_input_stream, iter_json_stream


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), default=None, help="Путь к входному файлу (JSON или NDJSON). Если не указан, читаем stdin.")
@click.option("--ndjson", is_flag=True, default=False, help="Флаг NDJSON. Если указан, читаем по одной JSON-записи на строку.")
@click.option("--path", "path_expr", type=str, default=None, help="Путь выборки, например: .items[*].price")
@click.option("--map", "map_spec", type=str, default=None, help="Map-операция: identity | pluck:key | to-number | length")
@click.option("--reduce", "reduce_spec", type=str, default=None, help="Reduce-операция: sum | count | max | min | first | last")
@click.option("-o", "output_path", type=click.Path(dir_okay=False), default=None, help="Путь для вывода результата (по умолчанию stdout)")
def main(input_path: Optional[str], ndjson: bool, path_expr: Optional[str], map_spec: Optional[str], reduce_spec: Optional[str], output_path: Optional[str]) -> None:
	"""CLI-обёртка для json-query.

	Читает поток JSON-объектов (NDJSON или массив), применяет фильтр по пути,
	затем map и reduce.
	"""
	input_stream = open_input_stream(input_path)
	try:
		items = iter_json_stream(input_stream, is_ndjson=ndjson)
		result = execute_query(items, path_expr=path_expr, map_spec=map_spec, reduce_spec=reduce_spec)
	finally:
		if input_stream is not sys.stdin:
			input_stream.close()

	if output_path:
		with open(output_path, "w", encoding="utf-8") as f:
			json.dump(result, f, ensure_ascii=False)
	else:
		json.dump(result, sys.stdout, ensure_ascii=False)
		sys.stdout.write("\n")


if __name__ == "__main__":
	main()


