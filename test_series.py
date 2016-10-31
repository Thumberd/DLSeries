import subAndRename

def test_extract_info1():
    text = "quantico.205.hdtv.addict7ed"
    season, episode = subAndRename.extract_info(text)
    assert season == '2'
    assert episode == '05'

def test_extract_info2():
    text = "quantico.505.hdtv.addict7ed.x264"
    season, episode = subAndRename.extract_info(text)
    assert season == '5'
    assert episode == '05'

def test_extract_info3():
    text = "Quantico - 02x03 - Stescalade"
    season, episode = subAndRename.extract_info(text)
    assert season == '02'
    assert episode == '03'

def test_extract_info4():
    text = "Quantico - S02E03 - Stescalade"
    season, episode = subAndRename.extract_info(text)
    assert season == '02'
    assert episode == '03'

def test_show1():
    text = "QuAnTICO"
    show = subAndRename.get_show(text)
    assert show == "Quantico"

def test_show2():
    text = "quantico"
    show = subAndRename.get_show(text)
    assert show == "Quantico"

def test_show3():
    text = "NCIS: Los Angeles"
    show = subAndRename.get_show(text)
    assert show == "NCIS Los Angeles"

def test_show4():
    text = "mr. robot"
    show = subAndRename.get_show(text)
    assert show == "Mr Robot"

def test_show5():
    text = "the.100"
    show = subAndRename.get_show(text)
    assert show == "The 100"