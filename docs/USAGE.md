# Использование json-query

## Установка

```bash
pip install -r requirements.txt
```

## Запуск справки

```bash
python -m json_query --help
```

## Примеры

- Выбор значений по пути и сумма:
```bash
python -m json_query --input examples/sample.json --path ".items[*].price" --map to-number --reduce sum
```

- Подсчёт строк NDJSON из stdin:
```bash
type examples/sample.ndjson | python -m json_query --ndjson --reduce count
```

- Перебор большого массива файла:
```bash
python -m json_query --input examples/large_array.json --path ".[*].user.id" --reduce count
```
