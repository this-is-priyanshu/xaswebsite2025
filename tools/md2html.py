import sys
import re

NUMRE = re.compile(r"( *)(\d+\.|[-+] +)")
LINRE = re.compile(r"(!{0,1})\[(.+?)\]\((.+?)\)")
EMPRE = re.compile(r"([\*\+]{1,3})(.+?)([\*\+]{1,3})")

class Text:
    def __init__(self, src):
        self.src = src

    def append(self, src):
        self.src += ' ' + src

    def __repr__(self):

        src = self.src.replace('  ', '<br>')
        src = re.sub(LINRE, lambda k: f'<a href= {k[3]}> {k[2]} </a>' if k[1] != '!' else f'<img src= {k[3]} alt= "{k[2]}">' , src)
        src = re.sub(EMPRE, lambda k: f'<em>{k[2]}</em>' if k[1] == '*' else f'<strong>{k[2]}</strong>' if k[1] == '**' else f'<span class=strong-em>{k[2]}</span>', src)

        return src

class Header:
    def __init__(self, src):
        self.text = Text(src.lstrip('#'))
        self.lvl = src.count('#') - str(self.text).count('#')

    def __repr__(self):
        if self.lvl <= 7:
            return f"<h{self.lvl}> {self.text} </h{self.lvl}>"
        else:
            return f"<strong class=header-{self.lvl}> {self.text} </strong>"

class List:
    def __init__(self, src):
        self.lst = []
        self.append(src)

    def append(self, src):
        config = NUMRE.match(src)
        text = NUMRE.sub('', src)
        self.lst += [{'lvl' : len(config.group(1)), 'text' : Text(text)}]

    def __repr__(self):
        cur = [0]
        src = ''

        src += "<ul>\n"
        for l in self.lst:
            if l['lvl'] == cur[-1]:
                src += f"<li> {l['text']} </li>\n"

            elif l['lvl'] < cur[-1]:
                src += "</ul>\n"
                src += f"<li> {l['text']} </li>\n"
                cur = cur[:-1]

            elif l['lvl'] > cur[-1]:
                cur = cur + [l['lvl']]
                src += "<ul>\n"
                src += f"<li> {l['text']} </li>\n"
        src += "</ul>\n"

        return src

class Chunk:
    def __init__(self, src):
        self.lines = src.split('\n')
        self.blocks = []

        self.parse()

    def parse(self):
        for i in self.lines:
            if i == '':
                pass

            elif i[0] == '#':
                self.blocks.append(Header(i))

            elif NUMRE.match(i) is not None:
                if len(self.blocks) >= 1 and isinstance(self.blocks[-1], List): 
                    self.blocks[-1].append(i)
                else:
                    self.blocks.append(List(i))

            else:
                if len(self.blocks) >= 1 and isinstance(self.blocks[-1], Text): 
                    self.blocks[-1].append(i)
                else:
                    self.blocks.append(Text(i))

    def __repr__(self):

        if self.blocks == []:
            return ""

        if isinstance(self.blocks[0], Header):
            return str(self.blocks[0])

        src = ''
        for b in self.blocks:
            src += str(b)
        return f"<p> {src} </p>"

class Markdown:
    def __init__(self, src):
        self.paragraphs = list(map(lambda x : Chunk(x), src.split('\n\n')))

    def assimilate(self):
        for c in self.paragraphs:
            l.parse()

    def __repr__(self):
        src = '<div>\n'
        for i in self.paragraphs:
            src += str(i) + '\n'
        return src + '</div>'


def main(inf, outf = None):
    src = open(inf).read()
    print(Markdown(src), file= sys.stdout if outf == None else open(outf, mode='w'))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: md2html.py inputfile [outputfile]')
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main(sys.argv[1], sys.argv[2])

