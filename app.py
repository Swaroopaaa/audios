import base64
from html import escape
import json
from pathlib import Path

import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "data" / "sentences.json"
AUDIO_DIR = PROJECT_DIR / "audio"


def load_sentences() -> list[dict[str, object]]:
    with DATA_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def audio_for_index(index: object) -> tuple[Path | None, bool]:
    matches = sorted(AUDIO_DIR.glob(f"{index}_*.wav"))
    if len(matches) == 1:
        return matches[0], False
    return None, len(matches) > 1


st.set_page_config(page_title="Telugu–English Clitic Dataset", page_icon="📚", layout="wide")
st.title("Telugu–English Clitic Dataset")

try:
    sentences = load_sentences()
except (OSError, json.JSONDecodeError) as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()

if not sentences:
    st.info("No sentences are available in the dataset.")
    st.stop()

sentences.sort(key=lambda sentence: int(sentence["Index"]))
st.caption(f"{len(sentences)} sentences")
table_rows = []
for sentence in sentences:
    index = sentence["Index"]
    audio_path, ambiguous = audio_for_index(index)
    if audio_path is not None:
        audio_data = base64.b64encode(audio_path.read_bytes()).decode("ascii")
        audio_cell = (
            f'<audio controls preload="none" aria-label="Audio for sentence '
            f'{escape(str(index))}"><source src="data:audio/wav;base64,{audio_data}" '
            'type="audio/wav"></audio>'
        )
    elif ambiguous:
        audio_cell = '<span class="audio-status">Multiple matching clips</span>'
    else:
        audio_cell = '<span class="audio-status">No audio available</span>'

    cells = [
        escape(str(index)),
        escape(str(sentence["English Sentence"])),
        escape(str(sentence["Telugu Sentence"])),
        escape(str(sentence["English Clitic Word"])),
        escape(str(sentence["Clitic"])),
        audio_cell,
    ]
    table_rows.append(
        "<tr>"
        f'<th scope="row" class="index-cell">{cells[0]}</th>'
        f"<td>{cells[1]}</td><td lang=\"te\">{cells[2]}</td>"
        f"<td>{cells[3]}</td><td>{cells[4]}</td>"
        f'<td class="audio-cell">{cells[5]}</td></tr>'
    )

dark_theme = st.get_option("theme.base") == "dark"
if dark_theme:
    palette = {
        "background": "#171b20",
        "header": "#262d34",
        "row": "#1c2228",
        "alternate": "#20272e",
        "hover": "#29363a",
        "border": "#39434b",
        "text": "#edf1f3",
        "muted": "#b3c0c5",
        "accent": "#8bd3c7",
    }
else:
    palette = {
        "background": "#ffffff",
        "header": "#edf2f3",
        "row": "#ffffff",
        "alternate": "#f6f8f8",
        "hover": "#edf6f4",
        "border": "#d8e0e2",
        "text": "#202a2d",
        "muted": "#5c6b70",
        "accent": "#176b62",
    }

table_html = f"""
<style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; color: {palette['text']}; font-family: sans-serif; }}
    .table-wrap {{ max-height: 720px; overflow: auto; border: 1px solid {palette['border']}; border-radius: 6px; }}
    table {{ width: 100%; min-width: 1060px; border-collapse: separate; border-spacing: 0; table-layout: fixed; background: {palette['background']}; }}
    thead th {{ position: sticky; top: 0; z-index: 1; background: {palette['header']}; color: {palette['text']}; text-align: left; font-size: 13px; font-weight: 650; }}
    th, td {{ padding: 14px 12px; border-bottom: 1px solid {palette['border']}; vertical-align: middle; overflow-wrap: anywhere; line-height: 1.5; }}
    tbody td, tbody th {{ background: {palette['row']}; color: {palette['text']}; font-size: 14px; }}
    tbody tr:nth-child(even) td, tbody tr:nth-child(even) th {{ background: {palette['alternate']}; }}
    tbody tr:hover td, tbody tr:hover th {{ background: {palette['hover']}; }}
    tbody tr:last-child td, tbody tr:last-child th {{ border-bottom: 0; }}
    th:nth-child(1) {{ width: 6%; }}
    th:nth-child(2), th:nth-child(3) {{ width: 22%; }}
    th:nth-child(4) {{ width: 15%; }}
    th:nth-child(5) {{ width: 8%; }}
    th:nth-child(6) {{ width: 27%; }}
    .index-cell {{ color: {palette['accent']}; font-variant-numeric: tabular-nums; font-weight: 700; }}
    .audio-cell {{ min-width: 230px; }}
    audio {{ display: block; width: 100%; height: 40px; }}
    .audio-status {{ color: {palette['muted']}; font-size: 13px; }}
</style>
<div class="table-wrap">
  <table>
    <thead><tr>
      <th scope="col">Index</th>
      <th scope="col">English Sentence</th>
      <th scope="col">Telugu Sentence</th>
      <th scope="col">English Clitic Word</th>
      <th scope="col">Clitic</th>
      <th scope="col">Audio</th>
    </tr></thead>
    <tbody>{''.join(table_rows)}</tbody>
  </table>
</div>
"""
st.components.v1.html(table_html, height=760, scrolling=True)