#!/usr/bin/python3

class Text(str):
    def __str__(self) -> str:
        replace_list = [
            ["<", "&lt;"],
            [">", "&gt;"],
            ["\n", "\n<br />\n"],
            ["\"", "&quot;"]
        ]
        result = super().__str__()
        for r in replace_list:
            result = result.replace(r[0], r[1])
        return result

class Elem:
    
    class ValidationError(Exception):
        def __init__(self) -> None:
            super().__init__("Incorrect data")

    def __init__(self, tag='div', attr: dict = {}, content=None, tag_type='double'):

        self.attr = attr
        self.content = []
        self.tag = tag
        if not (self.check_type(content) or content is None):
            raise self.ValidationError
        if content:
            self.add_content(content)
        elif content is not None:   
            self.content.append(content)
        if (tag_type != "double" and tag_type != "simple"):
            raise self.ValidationError
        self.tag_type = tag_type

    def __str__(self) -> str:
        attr = self.__make_attr()
        res = "<{tag}{attr}".format(tag=self.tag, attr=attr)
        if self.tag_type == "double":
            res += ">{cont}</{tag}>".format(cont=self.__make_content(), tag=self.tag)
        elif self.tag_type == "simple":
            res += " />"
        return res

    def __make_attr(self):
        result = ""
        for pair in sorted(self.attr.items()):
            result += " " + str(pair[0]) + "=\"" + str(pair[1]) + "\""
        return result

    def __make_content(self):
        if len(self.content) == 0:
            return ""
        result = "\n"
        for elem in self.content:
            if len(str(elem)) != 0:
                result += "{elem}\n".format(elem=elem)
        result = "  ".join(line for line in result.splitlines(True))
        if len(result.strip()) == 0:
            return ""
        return result     

    def add_content(self, content):
        if not Elem.check_type(content):
            raise Elem.ValidationError
        if type(content) == list:
            self.content += [elem for elem in content if elem != Text('')]
        elif content != Text(''):
            self.content.append(content)
        
        
    @staticmethod
    def check_type(content):
        return (isinstance(content, Elem) or type(content) == Text or
                (type(content) == list and all([type(elem) == Text or
                                                isinstance(elem, Elem)
                                                for elem in content])))

if __name__ == "__main__":
    elem = Elem(
        tag="html",
        content=[
            Elem(
                tag="head",
                content=[Elem(tag="title", content=Text('"Hello ground!"'))],
            ),
            Elem(
                tag="body",
                content=[
                    Elem(tag="h1", content=Text('"Oh no, not again!"')),
                    Elem(
                        tag="img",
                        attr={"src": "http://i.imgur.com/pfp3T.jpg"},
                        tag_type="simple",
                    ),
                ],
            ),
        ],
    )
    print(elem)