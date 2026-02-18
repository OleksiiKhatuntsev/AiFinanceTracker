from parsers.merchant import classify_merchant


def test_bea_apple_pay():
    desc = "BEA, Apple Pay Albert Heijn 1276,PAS541"
    assert classify_merchant(desc) == "Albert Heijn 1276"


def test_bea_betaalpas():
    desc = "BEA, Betaalpas NEU Vendingland,PAS541"
    assert classify_merchant(desc) == "NEU Vendingland"


def test_ecom_apple_pay():
    desc = "eCom, Apple Pay Revolut**9547*"
    assert classify_merchant(desc) == "Revolut"


def test_sepa_transfer():
    desc = "/TRTP/SEPA OVERBOEKING/IBAN/NL13ABNA/BIC/ABNANL2A/NAME/Oleksii Khatuntsev/REMI/test"
    assert classify_merchant(desc) == "Oleksii Khatuntsev"


def test_sepa_incasso():
    desc = "/TRTP/SEPA Incasso algemeen doorlopend/CSID/LU96ZZZ0000000000000000058/NAME/SpotifyAB/REMI/test"
    assert classify_merchant(desc) == "SpotifyAB"


def test_fallback_truncates():
    long_desc = "A" * 80
    result = classify_merchant(long_desc)
    assert result == "A" * 60
    assert len(result) == 60
