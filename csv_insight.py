"""
CSV Insight — análisis de CSV con stdlib (sin pandas).
Uso: python csv_insight.py sample.csv
"""
from __future__ import annotations

import argparse
import csv
import statistics
from collections import Counter
from pathlib import Path


def load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = reader.fieldnames or []
    return fields, rows


def is_number(v: str) -> bool:
    try:
        float(v.replace(",", ""))
        return True
    except ValueError:
        return False


def analyze(fields: list[str], rows: list[dict[str, str]]) -> str:
    lines = [
        f"Archivo: {len(rows)} filas · {len(fields)} columnas",
        f"Columnas: {', '.join(fields)}",
        "",
    ]
    for col in fields:
        values = [r.get(col, "") for r in rows if r.get(col, "") != ""]
        missing = len(rows) - len(values)
        nums = [float(v.replace(",", "")) for v in values if is_number(v)]
        lines.append(f"## {col}")
        lines.append(f"  no nulos: {len(values)} · faltantes: {missing}")
        if len(nums) >= max(3, int(len(values) * 0.6)):
            lines.append(f"  tipo: numérico")
            lines.append(f"  min={min(nums):.2f} max={max(nums):.2f} media={statistics.mean(nums):.2f}")
            if len(nums) > 1:
                lines.append(f"  desv={statistics.pstdev(nums):.2f}")
        else:
            top = Counter(values).most_common(5)
            lines.append("  tipo: categórico / texto")
            lines.append("  top valores:")
            for val, n in top:
                lines.append(f"    - {val!r}: {n}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Insights rápidos sobre un CSV")
    parser.add_argument("csv_path", type=Path, help="Ruta al archivo CSV")
    args = parser.parse_args()
    if not args.csv_path.exists():
        raise SystemExit(f"No existe: {args.csv_path}")
    fields, rows = load_rows(args.csv_path)
    print(analyze(fields, rows))


if __name__ == "__main__":
    main()
