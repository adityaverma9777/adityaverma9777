import os
import html

HERE = os.path.dirname(os.path.abspath(__file__))
ASCII_FILE = os.path.join(HERE, "..", "ascii-art.txt")
with open(ASCII_FILE, "r", encoding="utf-8") as f:
    ascii_rows = [line.rstrip("\n") for line in f.readlines()]
while ascii_rows and not ascii_rows[-1].strip():
    ascii_rows.pop()
ascii_rows = ascii_rows[17:]

ASCII_FONT = 8
ASCII_LINE_H = 11
ASCII_X = 15
ASCII_Y0 = 12

INFO_X = 510
INFO_Y0 = 25
INFO_LINE_H = 22
INFO_FONT = 16

CANVAS_W = 1200
CANVAS_H = max(len(ascii_rows) * ASCII_LINE_H + ASCII_Y0 + 20, 22 * INFO_LINE_H + INFO_Y0 + 30)

VALUE_COL = 35


def dots(key_display_len):
    n = max(1, VALUE_COL - key_display_len - 5)
    return " " + "." * n + " "


def kv_line(info_x, y, key, value, key2=None, val_id=None, dots_id=None,
            key_col=None, val_col=None, cc_col=None, fg=None):
    id_attr = f' id="{val_id}"' if val_id else ""
    did_attr = f' id="{dots_id}"' if dots_id else ""
    key_len = len(key) + (1 + len(key2) if key2 else 0) + 1
    dot_str = dots(key_len)
    if key2:
        k_part = (
            f'<tspan class="key">{html.escape(key)}</tspan>'
            f'.<tspan class="key">{html.escape(key2)}</tspan>:'
        )
    else:
        k_part = f'<tspan class="key">{html.escape(key)}</tspan>:'
    return (
        f'<tspan x="{info_x}" y="{y}" class="cc">. </tspan>'
        f'{k_part}'
        f'<tspan class="cc"{did_attr}>{html.escape(dot_str)}</tspan>'
        f'<tspan class="value"{id_attr}>{html.escape(value)}</tspan>'
    )


def make_svg(theme):
    if theme == "dark":
        bg, fg = "#161b22", "#c9d1d9"
        ascii_fg = "#c9d1d9"
        key_col, val_col, add_col, del_col, cc_col = "#ffa657", "#a5d6ff", "#3fb950", "#f85149", "#616e7f"
    else:
        bg, fg = "#f6f8fa", "#24292f"
        ascii_fg = "#24292f"
        key_col, val_col, add_col, del_col, cc_col = "#953800", "#0a3069", "#1a7f37", "#cf222e", "#9e9e9e"

    def y(i):
        return INFO_Y0 + i * INFO_LINE_H

    parts = []
    parts.append("<?xml version='1.0' encoding='UTF-8'?>")
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'font-family="ConsolasFallback,Consolas,monospace" '
        f'width="{CANVAS_W}px" height="{CANVAS_H}px" font-size="{INFO_FONT}px">'
    )
    parts.append(f"""<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {key_col};}}
.value {{fill: {val_col};}}
.addColor {{fill: {add_col};}}
.delColor {{fill: {del_col};}}
.cc {{fill: {cc_col};}}
.ascii {{font-size: {ASCII_FONT}px;}}
text, tspan {{white-space: pre;}}
</style>""")
    parts.append(f'<rect width="{CANVAS_W}px" height="{CANVAS_H}px" fill="{bg}" rx="15"/>')

    parts.append(f'<text x="{ASCII_X}" y="{ASCII_Y0}" fill="{ascii_fg}" class="ascii">')
    for i, row_txt in enumerate(ascii_rows):
        ry = ASCII_Y0 + i * ASCII_LINE_H
        parts.append(f'<tspan x="{ASCII_X}" y="{ry}">{html.escape(row_txt)}</tspan>')
    parts.append('</text>')

    parts.append(f'<text x="{INFO_X}" y="{INFO_Y0}" fill="{fg}">')

    DASH = "\u2014" * 33 + "-\u2014-"
    parts.append(f'<tspan x="{INFO_X}" y="{y(0)}">adityaverma9777@github</tspan> -{DASH}')

    parts.append(kv_line(INFO_X, y(1), "OS", "Windows 11, Android 14"))
    parts.append(kv_line(INFO_X, y(2), "Uptime", "calculating...", val_id="age_data", dots_id="age_data_dots"))
    parts.append(kv_line(INFO_X, y(3), "Focus", "ML Systems & Inference Eng."))
    parts.append(kv_line(INFO_X, y(4), "Edu", "BCA \u2014 Computer Applications"))
    parts.append(kv_line(INFO_X, y(5), "IDE", "VSCode, PyCharm"))
    parts.append(f'<tspan x="{INFO_X}" y="{y(6)}" class="cc">. </tspan>')
    parts.append(kv_line(INFO_X, y(7), "Languages", "Python, TypeScript, Java, C++", key2="Programming"))
    parts.append(kv_line(INFO_X, y(8), "Languages", "HTML, CSS, JSON, YAML", key2="Computer"))
    parts.append(f'<tspan x="{INFO_X}" y="{y(9)}" class="cc">. </tspan>')
    parts.append(kv_line(INFO_X, y(10), "Interests", "Inference Opt., PyTorch, HF", key2="AI"))
    parts.append(kv_line(INFO_X, y(11), "Interests", "FastAPI, Redis, PostgreSQL", key2="Backend"))

    CDASH = "\u2014" * 30 + "-\u2014-"
    parts.append(f'<tspan x="{INFO_X}" y="{y(12)}">- Contact</tspan> -{CDASH}')

    parts.append(kv_line(INFO_X, y(13), "Email", "adityaverma9777@gmail.com"))
    parts.append(kv_line(INFO_X, y(14), "Portfolio", "adityavermaworks.in"))
    parts.append(kv_line(INFO_X, y(15), "LinkedIn", "adityaverma9777"))
    parts.append(kv_line(INFO_X, y(16), "Instagram", "chaii.samosa"))

    GDASH = "\u2014" * 26 + "-\u2014-"
    parts.append(f'<tspan x="{INFO_X}" y="{y(17)}">- GitHub Stats</tspan> -{GDASH}')

    repo_dots = dots(len("Repos") + 1)
    star_dots = dots(len("Stars") + 1)
    parts.append(
        f'<tspan x="{INFO_X}" y="{y(18)}" class="cc">. </tspan>'
        f'<tspan class="key">Repos</tspan>:'
        f'<tspan class="cc" id="repo_data_dots">{html.escape(repo_dots)}</tspan>'
        f'<tspan class="value" id="repo_data">-</tspan>'
        f' {{<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">-</tspan>}}'
        f' | <tspan class="key">Stars</tspan>:'
        f'<tspan class="cc" id="star_data_dots">{html.escape(star_dots)}</tspan>'
        f'<tspan class="value" id="star_data">-</tspan>'
    )
    commit_dots = dots(len("Commits") + 1)
    follower_dots = dots(len("Followers") + 1)
    parts.append(
        f'<tspan x="{INFO_X}" y="{y(19)}" class="cc">. </tspan>'
        f'<tspan class="key">Commits</tspan>:'
        f'<tspan class="cc" id="commit_data_dots">{html.escape(commit_dots)}</tspan>'
        f'<tspan class="value" id="commit_data">-</tspan>'
        f' | <tspan class="key">Followers</tspan>:'
        f'<tspan class="cc" id="follower_data_dots">{html.escape(follower_dots)}</tspan>'
        f'<tspan class="value" id="follower_data">-</tspan>'
    )
    parts.append('</text>')
    parts.append('</svg>')
    return "\n".join(parts)


dark_svg = make_svg("dark")
light_svg = make_svg("light")

dark_path = os.path.join(HERE, "dark_mode.svg")
light_path = os.path.join(HERE, "light_mode.svg")

with open(dark_path, "w", encoding="utf-8") as f:
    f.write(dark_svg)
with open(light_path, "w", encoding="utf-8") as f:
    f.write(light_svg)

print(f"Canvas: {CANVAS_W} x {CANVAS_H}")
print(f"wrote dark_mode.svg  ({len(dark_svg):,} bytes)")
print(f"wrote light_mode.svg ({len(light_svg):,} bytes)")
