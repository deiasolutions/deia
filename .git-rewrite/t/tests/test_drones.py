from src.deia.drones import (
    ReaderDrone,
    SummarizerDrone,
    ArchitectDrone,
    WriterDrone,
    StylistDrone,
    ScribeDrone,
)
from src.deia.orchestrator import run_clock


def test_drone_classes_import_and_basic_methods():
    r = ReaderDrone(name="reader", role="Reader")
    text = r.ingest(__file__)
    headers = r.tag_sections(text)

    s = SummarizerDrone(name="summarizer", role="Summarizer")
    summary = s.summarize(headers)

    a = ArchitectDrone(name="architect", role="Architect")
    deps = a.map_dependencies(headers)
    prop = a.propose(headers)

    w = WriterDrone(name="writer", role="Writer")
    draft = w.compose(prop)

    st = StylistDrone(name="stylist", role="Stylist")
    formatted = st.format(draft)
    quality = st.check_quality(formatted)

    sc = ScribeDrone(name="scribe", role="Scribe")
    path = sc.commit(".deia/tmp/test_output.md", formatted)

    assert isinstance(text, str)
    assert isinstance(headers, list)
    assert isinstance(summary, str)
    assert isinstance(deps, dict)
    assert isinstance(prop, list)
    assert isinstance(draft, str)
    assert isinstance(formatted, str)
    assert isinstance(quality, dict)
    assert path.endswith("test_output.md")


def test_orchestrator_runs_ticks():
    r = ReaderDrone(name="reader", role="Reader")
    s = SummarizerDrone(name="summarizer", role="Summarizer")
    run_clock([r, s], clock_interval=0.0, ticks=3)
