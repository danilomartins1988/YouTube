from hiddeneco.research import formatting as f


def test_usd_rough_rounds_honestly():
    assert f.usd_rough(99557) == "almost 100,000 dollars"
    assert f.usd_rough(81249) == "roughly 81,200 dollars"


def test_ratio_words():
    assert f.ratio_words(1.86) == "almost twice"
    assert f.ratio_words(2.44) == "about two and a half times"
    assert f.ratio_words(2.15) == "more than twice"
    assert f.ratio_words(1.25) == "about 1.2 times" or f.ratio_words(1.25) == "about 1.3 times"


def test_display_formats():
    assert f.usd(99557.4) == "$99,557"
    assert f.millions(8888822) == "8.9 million"
    assert f.ratio(1.861) == "1.9×"
