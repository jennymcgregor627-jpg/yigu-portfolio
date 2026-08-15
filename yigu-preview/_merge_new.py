# -*- coding: utf-8 -*-
"""将 _analyses_w16_40.json 的内容追加到 _data.json。"""
import json, io, os

BASE = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE, "_data.json")
new_path = os.path.join(BASE, "_analyses_w16_40.json")

with io.open(new_path, encoding="utf-8-sig") as f:
    new_items = json.load(f)

with io.open(data_path, encoding="utf-8-sig") as f:
    data = json.load(f)

existing_ids = {a["id"] for a in data}
added = 0
for item in new_items:
    if item["id"] not in existing_ids:
        data.append(item)
        added += 1
        print("追加: %s (%s)" % (item["id"], item["name"]))

with io.open(data_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("完成: 追加 %d 件, _data.json 现有 %d 件" % (added, len(data)))
