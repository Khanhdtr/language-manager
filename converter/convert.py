import yaml, json, os, subprocess

SRC = "../languages"
OUT_FLUTTER = "./flutter_output"
OUT_QML = "./qml_output"

os.makedirs(OUT_FLUTTER, exist_ok=True)
os.makedirs(OUT_QML, exist_ok=True)

def load_yaml(path):
    with open(path, "r", encoding="utf8") as f:
        return yaml.safe_load(f)

def to_arb(lang, data):
    arb = {"@@locale": lang}
    for k, v in data.items():
        v = v.replace("%1", "{arg1}")
        arb[k] = v
    return arb

def to_ts(lang, data):
    xml = f'<TS version="2.1" language="{lang}">\n  <context>\n    <name>app</name>\n'
    for k, v in data.items():
        xml += f'    <message>\n      <source>{k}</source>\n      <translation>{v}</translation>\n    </message>\n'
    xml += '  </context>\n</TS>'
    return xml

langs = ["en", "vi"]
for lang in langs:
    src_path = f"{SRC}/{lang}.yaml"
    data = load_yaml(src_path)

    # Flutter output
    arb_path = f"{OUT_FLUTTER}/app_{lang}.arb"
    with open(arb_path, "w", encoding="utf8") as f:
        json.dump(to_arb(lang, data), f, ensure_ascii=False, indent=2)

    # QML output
    ts_path = f"{OUT_QML}/{lang}.ts"
    with open(ts_path, "w", encoding="utf8") as f:
        f.write(to_ts(lang, data))

print("Done.")
