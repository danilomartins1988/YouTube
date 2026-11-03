from hiddeneco import script as s
from hiddeneco import storyboard as sb
from hiddeneco.models import Script, Segment


def test_project_scripts_have_no_sourcing_errors(paths, dossier):
    assert paths.deliverables() == ["horizontal", "vertical"]
    for name in paths.deliverables():
        sc = s.load_script(paths.for_deliverable(name).deliverable_dir)
        errors = [i for i in s.sourcing_issues(sc, dossier) if i["severity"] == "error"]
        assert errors == [], name


def test_cap_filter(dossier):
    assert s.render_text("{{pharma_share_2024|cap}} of it", dossier) == "More than half of it"


def test_numbers_come_from_dossier(dossier):
    text = s.render_text("It produced {{gdppc_che_2023}} in {{gdppc_che_2023.year}}.", dossier)
    assert text == "It produced almost 100,000 dollars in 2023."


def test_hand_typed_digits_are_errors(dossier):
    sc = Script(title="t", segments=[Segment(id="a", narration="GDP grew 7% last year.")])
    issues = s.sourcing_issues(sc, dossier)
    assert any(i["severity"] == "error" and "digits" in i["message"] for i in issues)


def test_number_words_are_flagged(dossier):
    sc = Script(title="t", segments=[Segment(id="a", narration="Exports doubled to a million tonnes.")])
    issues = s.sourcing_issues(sc, dossier)
    assert any("million" in i["message"] for i in issues)


def test_undeclared_placeholder_is_error(dossier):
    sc = Script(title="t", segments=[Segment(id="a", narration="{{pop_che_2023}} people.", claims=[])])
    assert any("not listed" in i["message"] for i in s.sourcing_issues(sc, dossier))


def test_storyboard_values_resolve(hpaths, vpaths, dossier):
    board = sb.rendered(sb.load_storyboard(hpaths.deliverable_dir), dossier)
    bars = next(x for x in board.scenes if x.type == "bar_chart")
    assert isinstance(bars.params["data"], list) and bars.params["data"][0]["code"] == "CHE"
    for p in (hpaths, vpaths):
        board = sb.load_storyboard(p.deliverable_dir)
        assert sb.check_alignment(board, s.load_script(p.deliverable_dir)) == []
