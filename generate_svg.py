import os
import html

HERE = os.path.dirname(os.path.abspath(__file__))

INFO_X = 510
INFO_Y0 = 25
INFO_LINE_H = 22
INFO_FONT = 16
CANVAS_W = 1200
CANVAS_H = 22 * INFO_LINE_H + INFO_Y0 + 30

VALUE_COL = 35

CX = INFO_X // 2
CY = CANVAS_H // 2


def dots(key_display_len):
    n = max(1, VALUE_COL - key_display_len - 5)
    return " " + "." * n + " "


def kv_line(info_x, y, key, value, key2=None, val_id=None, dots_id=None):
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


def pulse_rings(cx, cy, color1, color2, color3):
    NUM = 5
    DURATION = 4.0
    R_START = 6
    R_END = min(cx - 10, cy - 10)
    out = []
    for i in range(NUM):
        delay = f"-{i * DURATION / NUM:.2f}s"
        dasharray = f"{3 + i % 3} {4 + i % 4}"
        col = [color1, color2, color1, color3, color2][i]
        sw_start = 2.5 - i * 0.2
        sw_end = 0.4
        out.append(f"""<circle cx="{cx}" cy="{cy}" r="{R_START}" fill="none"
  stroke="{col}" stroke-dasharray="{dasharray}" stroke-width="{sw_start}" opacity="0.9">
  <animate attributeName="r" from="{R_START}" to="{R_END}" dur="{DURATION}s" begin="{delay}" repeatCount="indefinite" calcMode="ease"/>
  <animate attributeName="opacity" from="0.9" to="0" dur="{DURATION}s" begin="{delay}" repeatCount="indefinite" calcMode="ease"/>
  <animate attributeName="stroke-width" from="{sw_start}" to="{sw_end}" dur="{DURATION}s" begin="{delay}" repeatCount="indefinite" calcMode="ease"/>
</circle>""")
    out.append(f"""<circle cx="{cx}" cy="{cy}" r="{R_START * 3}" fill="none"
  stroke="{color3}" stroke-dasharray="1 8" stroke-width="1" opacity="0.4">
  <animate attributeName="r" from="{R_START * 3}" to="{R_END // 2}" dur="{DURATION * 0.7:.2f}s" begin="0s" repeatCount="indefinite" calcMode="ease"/>
  <animate attributeName="opacity" from="0.4" to="0" dur="{DURATION * 0.7:.2f}s" begin="0s" repeatCount="indefinite" calcMode="ease"/>
</circle>
<circle cx="{cx}" cy="{cy}" r="{R_START * 3}" fill="none"
  stroke="{color3}" stroke-dasharray="1 8" stroke-width="1" opacity="0.4">
  <animate attributeName="r" from="{R_START * 3}" to="{R_END // 2}" dur="{DURATION * 0.7:.2f}s" begin="-{DURATION * 0.35:.2f}s" repeatCount="indefinite" calcMode="ease"/>
  <animate attributeName="opacity" from="0.4" to="0" dur="{DURATION * 0.7:.2f}s" begin="-{DURATION * 0.35:.2f}s" repeatCount="indefinite" calcMode="ease"/>
</circle>""")
    out.append(f"""<circle cx="{cx}" cy="{cy}" r="4" fill="{color1}" opacity="0.9">
  <animate attributeName="opacity" values="0.9;1;0.5;1;0.9" dur="2s" repeatCount="indefinite"/>
  <animate attributeName="r" values="4;6;4" dur="2s" repeatCount="indefinite"/>
</circle>""")
    return "\n".join(out)


def make_svg(theme):
    if theme == "dark":
        bg, fg = "#161b22", "#c9d1d9"
        key_col, val_col = "#ffa657", "#a5d6ff"
        add_col, del_col, cc_col = "#3fb950", "#f85149", "#616e7f"
        p1, p2, p3 = "#ffa657", "#a5d6ff", "#3fb950"
    else:
        bg, fg = "#f6f8fa", "#24292f"
        key_col, val_col = "#953800", "#0a3069"
        add_col, del_col, cc_col = "#1a7f37", "#cf222e", "#9e9e9e"
        p1, p2, p3 = "#953800", "#0a3069", "#1a7f37"

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
text, tspan {{white-space: pre;}}
</style>""")
    parts.append(f'<rect width="{CANVAS_W}px" height="{CANVAS_H}px" fill="{bg}" rx="15"/>')
    parts.append(f'<rect width="{INFO_X}px" height="{CANVAS_H}px" fill="{bg}" rx="15"/>')
    parts.append(f'<line x1="{INFO_X - 1}" y1="15" x2="{INFO_X - 1}" y2="{CANVAS_H - 15}" stroke="{cc_col}" stroke-width="0.5" opacity="0.4"/>')
    parts.append(pulse_rings(CX, CY, p1, p2, p3))
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
