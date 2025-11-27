import yaml, json, os

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
    data = load_yaml(f"{SRC}/{lang}.yaml")

    with open(f"{OUT_FLUTTER}/app_{lang}.arb", "w", encoding="utf8") as f:
        json.dump(to_arb(lang, data), f, ensure_ascii=False, indent=2)

    with open(f"{OUT_QML}/{lang}.ts", "w", encoding="utf8") as f:
        f.write(to_ts(lang, data))

print("Done.")
