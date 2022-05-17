#!/usr/bin/python3

def parse_line(line: str):
    array = line.split('=')
    res = (val.strip().split(":") for val in array[1].split(','))
    res = dict(res)
    res["name"] = array[0].strip()
    return res


def periodic_table():
    HTML = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>periodic_table</title>
        <style>
            table{{
            border-collapse: collapse;
            }}
            h4 {{
            text-align: center;
            }}
            ul {{
            list-style:none;
            padding-left:0px;
            }}
        </style>
        </head>
        <body>
        <table>
            {body}
        </table>
        </body>
        </html>
            """
    TEMPLATE = """
        <td style="border: 1px solid black; padding:10px">
            <h4>{name}</h4>
            <ul>
            <li>No {number}</li>
            <li>{small}</li>
            <li>{molar}</li>
            <li>{electron} electron</li>
            </ul>
        </td>
                """

    body = "<tr>"
    with open("periodic_table.txt", "r") as file:
        period_table = (parse_line(line) for line in file.readlines())
    pos = 0
    for str in period_table:
        if pos > int(str["position"]):
            pos = 0
            body += "    </tr>\n    <tr>"
        for x in range(pos, int(str["position"]) - 1):
            body += "      <td></td>\n"
        pos = int(str["position"])
        body += TEMPLATE.format(
            name=str["name"],
            number=str["number"],
            small=str["small"],
            molar=str["molar"],
            electron=str["electron"],
        )
    
    body += "    </tr>\n"
    with open("periodic_table.html", "w") as file:
        file.write(HTML.format(body=body))

if __name__ == '__main__':
    periodic_table()