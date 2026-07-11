import os
import html

HERE = os.path.dirname(os.path.abspath(__file__))
ASCII_FILE = os.path.join(HERE, "..", "ascii-art.txt")
with open(ASCII_FILE, "r", encoding="utf-8") as f:
    ascii_rows = [line.rstrip("\n") for line in f.readlines()]
while ascii_rows and not ascii_rows[-1].strip():
    ascii_rows.pop()

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


def make_svg(theme):
    if theme == "dark":
        bg = "#161b22"
        fg = "#c9d1d9"
        ascii_fg = "#c9d1d9"
        key_col = "#ffa657"
        val_col = "#a5d6ff"
        add_col = "#3fb950"
        del_col = "#f85149"
        cc_col = "#616e7f"
    else:
        bg = "#f6f8fa"
        fg = "#24292f"
        ascii_fg = "#24292f"
        key_col = "#953800"
        val_col = "#0a3069"
        add_col = "#1a7f37"
        del_col = "#cf222e"
        cc_col = "#9e9e9e"

    def row(i):
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
.ascii {{font-size: {ASCII_FONT}px; line-height: {ASCII_LINE_H}px;}}
text, tspan {{white-space: pre;}}
</style>""")
    parts.append(f'<rect width="{CANVAS_W}px" height="{CANVAS_H}px" fill="{bg}" rx="15"/>')

    parts.append(f'<text x="{ASCII_X}" y="{ASCII_Y0}" fill="{ascii_fg}" class="ascii">')
    for i, row_txt in enumerate(ascii_rows):
        y = ASCII_Y0 + i * ASCII_LINE_H
        parts.append(f'<tspan x="{ASCII_X}" y="{y}">{html.escape(row_txt)}</tspan>')
    parts.append('</text>')

    parts.append(f'<text x="{INFO_X}" y="{INFO_Y0}" fill="{fg}">')

    DASH = "\u2014" * 35 + "-\u2014-"
    parts.append(f'<tspan x="{INFO_X}" y="{row(0)}">aditya@verma</tspan> -{DASH}')
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(1)}" class="cc">. </tspan>'
        f'<tspan class="key">OS</tspan>:'
        f'<tspan class="cc"> ....................... </tspan>'
        f'<tspan class="value">Windows 11, Android 14</tspan>'
    )
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(2)}" class="cc">. </tspan>'
        f'<tspan class="key">Uptime</tspan>:'
        f'<tspan class="cc" id="age_data_dots"> .................... </tspan>'
        f'<tspan class="value" id="age_data">calculating...</tspan>'
    )
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(3)}" class="cc">. </tspan>'
        f'<tspan class="key">Focus</tspan>:'
        f'<tspan class="cc"> ..................... </tspan>'
        f'<tspan class="value">ML Systems &amp; Inference Eng.</tspan>'
    )
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(4)}" class="cc">. </tspan>'
        f'<tspan class="key">Edu</tspan>:'
        f'<tspan class="cc"> ........................ </tspan>'
        f'<tspan class="value">BCA \u2014 Computer Applications</tspan>'
    )
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(5)}" class="cc">. </tspan>'
        f'<tspan class="key">IDE</tspan>:'
        f'<tspan class="cc"> ........................ </tspan>'
        f'<tspan class="value">VSCode, PyCharm</tspan>'
    )
    parts.append(f'<tspan x="{INFO_X}" y="{row(6)}" class="cc">. </tspan>')
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(7)}" class="cc">. </tspan>'
        f'<tspan class="key">Languages</tspan>.<tspan class="key">Programming</tspan>:'
        f'<tspan class="cc"> ..... </tspan>'
        f'<tspan class="value">Python, TypeScript, Java, C++</tspan>'
    )
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(8)}" class="cc">. </tspan>'
        f'<tspan class="key">Languages</tspan>.<tspan class="key">Computer</tspan>:'
        f'<tspan class="cc"> ......... </tspan>'
        f'<tspan class="value">HTML, CSS, JSON, YAML</tspan>'
    )
    parts.append(f'<tspan x="{INFO_X}" y="{row(9)}" class="cc">. </tspan>')
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(10)}" class="cc">. </tspan>'
        f'<tspan class="key">Interests</tspan>.<tspan class="key">AI</tspan>:'
        f'<tspan class="cc"> ........... </tspan>'
        f'<tspan class="value">Inference Opt., PyTorch, HF</tspan>'
    )
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(11)}" class="cc">. </tspan>'
        f'<tspan class="key">Interests</tspan>.<tspan class="key">Backend</tspan>:'
        f'<tspan class="cc"> .......... </tspan>'
        f'<tspan class="value">FastAPI, Redis, PostgreSQL</tspan>'
    )
    CDASH = "\u2014" * 32 + "-\u2014-"
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(12)}">- Contact</tspan> -{CDASH}'
    )
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(13)}" class="cc">. </tspan>'
        f'<tspan class="key">Email</tspan>:'
        f'<tspan class="cc"> .................... </tspan>'
        f'<tspan class="value">adityaverma9777@gmail.com</tspan>'
    )
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(14)}" class="cc">. </tspan>'
        f'<tspan class="key">Portfolio</tspan>:'
        f'<tspan class="cc"> ............... </tspan>'
        f'<tspan class="value">adityavermaworks.in</tspan>'
    )
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(15)}" class="cc">. </tspan>'
        f'<tspan class="key">LinkedIn</tspan>:'
        f'<tspan class="cc"> .................. </tspan>'
        f'<tspan class="value">adityaverma9777</tspan>'
    )
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(16)}" class="cc">. </tspan>'
        f'<tspan class="key">Instagram</tspan>:'
        f'<tspan class="cc"> ................. </tspan>'
        f'<tspan class="value">chaii.samosa</tspan>'
    )
    GDASH = "\u2014" * 28 + "-\u2014-"
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(17)}">- GitHub Stats</tspan> -{GDASH}'
    )
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(18)}" class="cc">. </tspan>'
        f'<tspan class="key">Repos</tspan>:'
        f'<tspan class="cc" id="repo_data_dots"> .... </tspan>'
        f'<tspan class="value" id="repo_data">-</tspan>'
        f' {{<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">-</tspan>}}'
        f' | <tspan class="key">Stars</tspan>:'
        f'<tspan class="cc" id="star_data_dots"> ........... </tspan>'
        f'<tspan class="value" id="star_data">-</tspan>'
    )
    parts.append(
        f'<tspan x="{INFO_X}" y="{row(19)}" class="cc">. </tspan>'
        f'<tspan class="key">Commits</tspan>:'
        f'<tspan class="cc" id="commit_data_dots"> ................. </tspan>'
        f'<tspan class="value" id="commit_data">-</tspan>'
        f' | <tspan class="key">Followers</tspan>:'
        f'<tspan class="cc" id="follower_data_dots"> ....... </tspan>'
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
print(f"ASCII rows: {len(ascii_rows)}, chars/row: {max(len(r) for r in ascii_rows)}")
print(f"wrote dark_mode.svg  ({len(dark_svg):,} bytes)")
print(f"wrote light_mode.svg ({len(light_svg):,} bytes)")
