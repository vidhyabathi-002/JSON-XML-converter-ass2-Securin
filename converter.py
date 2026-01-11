import json
import sys
import xml.sax.saxutils as saxutils

def escape(text):
    return saxutils.escape(str(text))

def convert(value, name=None):
    if isinstance(value, dict):
        if name:
            xml = f'<object name="{escape(name)}">'
        else:
            xml = "<object>"
        for k, v in value.items():
            xml += convert(v, k)
        xml += "</object>"
        return xml

    elif isinstance(value, list):
        xml = f'<array name="{escape(name)}">' if name else "<array>"
        for item in value:
            xml += convert(item)
        xml += "</array>"
        return xml

    elif isinstance(value, bool):
        return f'<boolean name="{escape(name)}">{str(value).lower()}</boolean>' if name else f'<boolean>{str(value).lower()}</boolean>'

    elif isinstance(value, int) or isinstance(value, float):
        return f'<number name="{escape(name)}">{value}</number>' if name else f'<number>{value}</number>'

    elif isinstance(value, str):
        return f'<string name="{escape(name)}">{escape(value)}</string>' if name else f'<string>{escape(value)}</string>'

    elif value is None:
        return f'<null name="{escape(name)}"/>' if name else "<null/>"

    else:
        raise TypeError("Unsupported JSON type")

def main():
    if len(sys.argv) != 3:
        print("Usage: python converter.py <input.json> <output.xml>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r") as f:
        data = json.load(f)

    if not isinstance(data, (dict, list)):
        print("Top-level JSON must be object or array")
        sys.exit(1)

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += convert(data)

    with open(output_file, "w") as f:
        f.write(xml)

    print("Conversion completed successfully")

if __name__ == "__main__":
    main()
