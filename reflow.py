import sys

def count_indent(line):
    if line.isspace():
        return None
    for i in range(0, len(line)):
        if not (line[i] == ' '):
            return i
    return None


if len(sys.argv) == 2:
    n = int(sys.argv[1])
else:
    sys.stderr.write("Usage:\n")
    sys.stderr.write("    cat infile | python reflow.py line-length > outfile\n")
    sys.stderr.write("E.g.,\n")
    sys.stderr.write("    cat infile | python reflow.py 80 > outfile\n")
    sys.exit()

def reflow_paragraph(lines_in, indent):
    failed = False
    words = []
    for line in lines_in:
        # Hard-coded: don't format lines that have [ or ]
        if line.find('[') >= 0 or line.find(']') >= 0:
            failed = True
            break
        cur_words = line.strip().split()
        if not (line == (indent * ' ') + (' '.join(cur_words))):
            sys.stderr.write("Warning, can't format: \"" + line + "\"\n")
            failed = True
        words.extend(cur_words)
    if failed:
        return lines_in

    lines = []
    cur_line = None
    for word in words:
        if cur_line is None:
            cur_line = (indent * ' ') + word
        else:
            if len(cur_line) + len(word) + 1 <= n:
                cur_line += ' '
                cur_line += word
            else:
                lines.append(cur_line)
                cur_line = (indent * ' ') + word
    if not (cur_line is None):
        lines.append(cur_line)
    return lines

xs = sys.stdin.readlines()

#Divide into paragraphs and reflow each one
lines = []
cur_paragraph = None
cur_indent = None
for x in xs:
    if len(x) > 0 and x[-1] == '\n':
        x = x[:-1]

    x_indent = count_indent(x)
    if cur_indent is None or not (cur_indent == x_indent):
        if not (cur_paragraph is None):
            lines.extend(reflow_paragraph(cur_paragraph, cur_indent))
        cur_indent = x_indent
        if x_indent is None:
            cur_paragraph = None
            lines.append(x)
        else:
            cur_paragraph = [x]
    else:
        cur_paragraph.append(x)

if not (cur_paragraph is None):
    lines.extend(reflow_paragraph(cur_paragraph, cur_indent))

for line in lines:
    print (line)
