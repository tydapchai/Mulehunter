import csv
from datetime import datetime, timezone

from mulehunter.graph import Transfer


IBM_CURRENCIES = {
    "Australian Dollar": "AUD", "Bitcoin": "BTC", "Brazil Real": "BRL",
    "Canadian Dollar": "CAD", "Euro": "EUR", "Mexican Peso": "MXN",
    "Ruble": "RUB", "Rupee": "INR", "Saudi Riyal": "SAR", "Shekel": "ILS",
    "Swiss Franc": "CHF", "UK Pound": "GBP", "US Dollar": "USD",
    "Yen": "JPY", "Yuan": "CNY",
}


def read_events(path, limit, stride=1, bounds=None):
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source)
        header = next(reader)
        accounts = [i for i, column in enumerate(header) if column.strip() == "Account"]
        if len(accounts) != 2:
            raise ValueError("Expected IBM AML CSV with two Account columns")
        columns = {name: index for index, name in enumerate(header)}
        if bounds:
            lower, upper = (value.strftime("%Y/%m/%d %H:%M") for value in bounds)
        for offset, row in enumerate(reader):
            if bounds and not lower <= row[columns["Timestamp"]] < upper:
                continue
            if offset % stride:
                continue
            if limit and len(rows) >= limit:
                break
            def field(name):
                return row[columns[name]].strip()
            timestamp = datetime.fromisoformat(field("Timestamp").replace("/", "-"))
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
            currency = field("Payment Currency")
            event = Transfer(str(offset), f'{field("From Bank")}:{row[accounts[0]]}',
                             f'{field("To Bank")}:{row[accounts[1]]}', float(field("Amount Paid")),
                             IBM_CURRENCIES.get(currency, currency), timestamp.timestamp())
            rows.append((event, int(field("Is Laundering"))))
    return sorted(rows, key=lambda item: item[0].timestamp)
