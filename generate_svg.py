import os
import html

HERE = os.path.dirname(os.path.abspath(__file__))

INFO_X = 510
INFO_Y0 = 25
INFO_LINE_H = 22
INFO_FONT = 16
CANVAS_W = 1250
CANVAS_H = 28 * INFO_LINE_H + INFO_Y0 + 30

VALUE_COL = 33

CX = INFO_X // 2
CY = CANVAS_H // 2


def dots(key_display_len):
    n = max(1, VALUE_COL - key_display_len - 5)
    return " " + "." * n + " "


def kv_line(info_x, y, key, value, key2=None, val_id=None, dots_id=None, link=None):
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
        
    if link:
        val_part = f'<a href="{html.escape(link)}" target="_blank"><tspan class="value link"{id_attr}>{html.escape(value)}</tspan></a>'
    else:
        val_part = f'<tspan class="value"{id_attr}>{html.escape(value)}</tspan>'
        
    return (
        f'<tspan x="{info_x}" y="{y}" class="cc">. </tspan>'
        f'{k_part}'
        f'<tspan class="cc"{did_attr}>{html.escape(dot_str)}</tspan>'
        f'{val_part}'
    )


def pulse_rings(cx, cy, color1, color2, color3, bg):
    out = []
    
    ease = 'calcMode="spline" keyTimes="0; 1" keySplines="0.165 0.84 0.44 1"'
    R_MAX = min(cx - 20, cy - 20)
    
    out.append(f'<g transform="translate({cx}, {cy})">')
    
    out.append(f'''<circle r="{R_MAX * 0.8}" fill="none" stroke="{color1}" stroke-width="1.5" stroke-dasharray="2 12" opacity="0.2">
  <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="40s" repeatCount="indefinite" />
</circle>''')
    out.append(f'''<circle r="{R_MAX * 0.6}" fill="none" stroke="{color2}" stroke-width="2" stroke-dasharray="1 6 4 6" opacity="0.3">
  <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="25s" repeatCount="indefinite" />
</circle>''')

    WAVE_COUNT = 4
    WAVE_DUR = 6.0
    for i in range(WAVE_COUNT):
        delay = f"-{i * (WAVE_DUR / WAVE_COUNT):.2f}s"
        out.append(f'''<circle r="0" fill="none" stroke="{color1}" stroke-width="1.5" opacity="0">
  <animate attributeName="r" values="10; {R_MAX}" dur="{WAVE_DUR}s" begin="{delay}" repeatCount="indefinite" {ease} />
  <animate attributeName="opacity" values="0.7; 0" dur="{WAVE_DUR}s" begin="{delay}" repeatCount="indefinite" {ease} />
</circle>''')
        
    RIPPLE_COUNT = 3
    RIPPLE_DUR = 3.0
    for i in range(RIPPLE_COUNT):
        delay = f"-{i * (RIPPLE_DUR / RIPPLE_COUNT):.2f}s"
        out.append(f'''<circle r="0" fill="none" stroke="{color3}" stroke-width="1" stroke-dasharray="4 4" opacity="0">
  <animate attributeName="r" values="5; {R_MAX * 0.7}" dur="{RIPPLE_DUR}s" begin="{delay}" repeatCount="indefinite" {ease} />
  <animate attributeName="opacity" values="0.5; 0" dur="{RIPPLE_DUR}s" begin="{delay}" repeatCount="indefinite" {ease} />
</circle>''')

    out.append(f'<circle r="16" fill="{color1}" opacity="0.15"><animate attributeName="r" values="14;18;14" dur="4s" repeatCount="indefinite" /></circle>')
    out.append(f'<circle r="10" fill="{color2}" opacity="0.25"><animate attributeName="r" values="9;11;9" dur="3s" repeatCount="indefinite" /></circle>')
    out.append(f'<circle r="5" fill="{color3}" opacity="0.8"><animate attributeName="opacity" values="0.5;1;0.5" dur="2s" repeatCount="indefinite" /></circle>')
    out.append(f'<circle r="2" fill="{bg}" opacity="0.9" />')

    out.append('</g>')
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
.link {{text-decoration: underline; cursor: pointer;}}
.link:hover {{fill: {add_col};}}
.addColor {{fill: {add_col};}}
.delColor {{fill: {del_col};}}
.cc {{fill: {cc_col};}}
text, tspan {{white-space: pre;}}
</style>""")
    parts.append(f'<rect width="{CANVAS_W}px" height="{CANVAS_H}px" fill="{bg}" rx="15"/>')
    parts.append(f'<rect width="{INFO_X}px" height="{CANVAS_H}px" fill="{bg}" rx="15"/>')
    parts.append(f'<line x1="{INFO_X - 1}" y1="15" x2="{INFO_X - 1}" y2="{CANVAS_H - 15}" stroke="{cc_col}" stroke-width="0.5" opacity="0.4"/>')
    parts.append(pulse_rings(CX, CY, p1, p2, p3, bg))
    parts.append(f'<text x="{INFO_X}" y="{INFO_Y0}" fill="{fg}">')

    DASH = "\u2014" * 38 + "-\u2014-"
    
    y_idx = 0
    parts.append(f'<tspan x="{INFO_X}" y="{y(y_idx)}">adityaverma9777@github</tspan> -{DASH}'); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "OS", "Windows 11, Android 14")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Uptime", "calculating...", val_id="age_data", dots_id="age_data_dots")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Focus", "ML Systems & Inference Eng.")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Edu", "BS (4 Years) Zoology Major (21-25)", key2="BS")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Edu", "BCA (26-29)", key2="BCA")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Hobbies", "Football, Cooking, Mountains")); y_idx+=1
    parts.append(f'<tspan x="{INFO_X}" y="{y(y_idx)}" class="cc">. </tspan>'); y_idx+=1
    
    parts.append(kv_line(INFO_X, y(y_idx), "Tech", "Python, TypeScript, JavaScript, Java, C++", key2="Languages")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Tech", "PyTorch, NumPy, Hugging Face", key2="AI/ML")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Tech", "FastAPI", key2="Backend")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Tech", "PostgreSQL, MongoDB", key2="Databases")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Tech", "Redis", key2="Caching")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Tech", "React, Next.js, Tailwind CSS, HTML5", key2="Frontend")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Tech", "Docker, Git", key2="DevOps")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Tech", "Google Cloud Platform", key2="Cloud")); y_idx+=1
    parts.append(f'<tspan x="{INFO_X}" y="{y(y_idx)}" class="cc">. </tspan>'); y_idx+=1
    
    parts.append(kv_line(INFO_X, y(y_idx), "Interests", "ML Systems, Inference Eng., Production AI, Deployment")); y_idx+=1

    CDASH = "\u2014" * 35 + "-\u2014-"
    parts.append(f'<tspan x="{INFO_X}" y="{y(y_idx)}">- Contact</tspan> -{CDASH}'); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Email", "adityaverma9777@gmail.com", link="mailto:adityaverma9777@gmail.com")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Portfolio", "https://www.adityavermaworks.in/", link="https://www.adityavermaworks.in/")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "LinkedIn", "https://linkedin.com/in/adityaverma9777", link="https://linkedin.com/in/adityaverma9777")); y_idx+=1
    parts.append(kv_line(INFO_X, y(y_idx), "Instagram", "https://instagram.com/chaii.samosa", link="https://instagram.com/chaii.samosa")); y_idx+=1

    GDASH = "\u2014" * 31 + "-\u2014-"
    parts.append(f'<tspan x="{INFO_X}" y="{y(y_idx)}">- GitHub Stats</tspan> -{GDASH}'); y_idx+=1

    repo_dots = dots(len("Repos") + 1)
    star_dots = dots(len("Stars") + 1)
    parts.append(
        f'<tspan x="{INFO_X}" y="{y(y_idx)}" class="cc">. </tspan>'
        f'<tspan class="key">Repos</tspan>:'
        f'<tspan class="cc" id="repo_data_dots">{html.escape(repo_dots)}</tspan>'
        f'<tspan class="value" id="repo_data">-</tspan>'
        f' {{<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">-</tspan>}}'
        f' | <tspan class="key">Stars</tspan>:'
        f'<tspan class="cc" id="star_data_dots">{html.escape(star_dots)}</tspan>'
        f'<tspan class="value" id="star_data">-</tspan>'
    )
    y_idx+=1
    commit_dots = dots(len("Commits") + 1)
    follower_dots = dots(len("Followers") + 1)
    parts.append(
        f'<tspan x="{INFO_X}" y="{y(y_idx)}" class="cc">. </tspan>'
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
