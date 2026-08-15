# -*- coding: utf-8 -*-
"""将 _data.json 中的 analyses 分析内容合并进 index.html 的内嵌 ARTIFACTS 数据。"""
import json, re, io, os

BASE = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(BASE, "index.html")
data_path = os.path.join(BASE, "_data.json")

with io.open(data_path, encoding="utf-8-sig") as f:
    full_data = json.load(f)
analyses_map = {a["id"]: a["analyses"] for a in full_data if a.get("analyses")}

with io.open(html_path, encoding="utf-8-sig") as f:
    html = f.read()

m = re.search(r"var ARTIFACTS = (\[.*?\]);", html, re.DOTALL)
if not m:
    raise SystemExit("未找到 ARTIFACTS 数组，中止。")

artifacts = json.loads(m.group(1))
merged = 0
for a in artifacts:
    if a["id"] in analyses_map and not a["analyses"]:
        a["analyses"] = analyses_map[a["id"]]
        merged += 1

new_raw = json.dumps(artifacts, ensure_ascii=False, indent=2)
html2 = html[: m.start(1)] + new_raw + html[m.end(1):]

with io.open(html_path, "w", encoding="utf-8") as f:
    f.write(html2)

print("已合并分析内容: %d 件" % merged)
print("剩余无分析内容: %d 件" % sum(1 for a in artifacts if not a["analyses"]))
