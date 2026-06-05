"""Your proprietary business logic.

This is the kind of module worth protecting — pricing rules, algorithms, the
parts you don't want shipped as readable source. `obfy build` obfuscates and
AES-256-GCM encrypts it; the plaintext never lands on the customer's disk.
"""


def pricing_quote(units: int) -> dict:
    base_unit_price = 49.0
    discount = 0.10 if units >= 10 else 0.0
    total = round(base_unit_price * units * (1 - discount), 2)
    return {
        "units": units,
        "unit_price": base_unit_price,
        "discount": discount,
        "total": total,
    }
