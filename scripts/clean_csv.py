import csv
import json
import pathlib
import re

DATA_DIR = pathlib.Path(__file__).resolve().parents[1]
OUTPUT_DIR = DATA_DIR / 'cleaned_data'
OUTPUT_DIR.mkdir(exist_ok=True)

# mapping function to canonical column names

def canonical(name):
    if not name:
        return ''
    key = name.strip().lower()
    key = re.sub(r'\s+', ' ', key)
    if key == 'hs':
        return 'hs'
    if key.startswith('sitc'):
        return 'sitc'
    if key == 'country':
        return 'country'
    if key == 'description':
        return 'description'
    if 'exports to usa' in key:
        return 'exports_usd'
    if 'quantity' in key:
        return 'quantity'
    if 'affected' in key:
        return 'affected'
    return key


def clean_numeric(val):
    val = val.strip()
    val = val.replace(',', '')
    if not val:
        return None
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return val


def process_file(path: pathlib.Path):
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = None
        for row in reader:
            if any('HS' == c.strip() for c in row):
                header = [canonical(c) for c in row if c.strip()]
                break
        if not header:
            raise ValueError(f'Header not found in {path}')
        rows = []
        for row in reader:
            if not any(c.strip() for c in row):
                continue
            # drop leading blank column
            if row and row[0].strip() == '':
                row = row[1:]
            row = [c.strip() for c in row]
            if len(row) != len(header):
                continue
            rec = dict(zip(header, row))
            if 'exports_usd' in rec:
                rec['exports_usd'] = clean_numeric(rec['exports_usd'])
            if 'quantity' in rec:
                rec['quantity'] = clean_numeric(rec['quantity'])
            rows.append(rec)
    out_file = OUTPUT_DIR / f'{path.stem}.json'
    with out_file.open('w', encoding='utf-8') as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    return out_file


def main():
    csv_paths = DATA_DIR.glob('*.csv')
    for csv_path in csv_paths:
        out_file = process_file(csv_path)
        print(f'Wrote {out_file}')


if __name__ == '__main__':
    main()
