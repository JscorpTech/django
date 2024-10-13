VARIABLE = "variable"
COMMENT = "comment"
ANOTHER = "another"


class Jst:
    def __init__(self, out_file, read_file=".env") -> None:
        self.data = {}
        self.out_file = out_file
        self.read_file = read_file

    def read_env(self):
        lines = {}
        with open(self.read_file, "r") as file:
            for number, line in enumerate(file.readlines()):
                strip_line = line.strip()
                variable = line.split("=")

                if strip_line.startswith("#"):
                    lines[number] = {
                        "type": COMMENT,
                        "data": line
                    }
                elif strip_line and len(variable) == 2:
                    lines[number] = {
                        "type": VARIABLE,
                        "key": variable[0],
                        "data": variable[1]
                    }
                else:
                    lines[number] = {
                        "type": ANOTHER,
                        "data": line
                    }
            self.data = lines
        return lines

    def write_env(self):
        with open(self.out_file, "w") as file:
            lines = []
            for number, line in self.data.items():
                if line['type'] == VARIABLE:
                    lines.append("{}={}".format(line["key"], line['data']))
                else:
                    lines.append(line['data'])
            file.writelines(lines)
        self.data = lines

    def comment(self, comment):
        self.edit(value="\n\n\n", item_type=ANOTHER)
        self.edit(value="\n# {}".format(comment), item_type=COMMENT)

    def edit(self, key=None, value=None, item_type=VARIABLE):
        data = self.read_env()
        find_data = list(filter(lambda item: True if item[1]['type'] == VARIABLE and item[1]['key'] == key else False, data.items()))
        if len(find_data) >= 1:
            data[find_data[0][0]]["data"] = value
        else:
            data[list(data.keys())[-1] + 1] = {
                "type": item_type,
                "key": "\n{}".format(key),
                "data": value
            }
        self.write_env()
        return data
