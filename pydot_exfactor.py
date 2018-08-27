import os

import pydot
import random
import itertools

from matplotlib import pyplot as plt
from matplotlib_venn import venn2
from PIL import Image, ImageFont, ImageDraw


class Node:
    def __init__(self, value):
        self.value = value
        self.nodes = [None, None]
        self.find_factors()

    def append_left(self, value):
        self.nodes[0] = Node(value)
        self.nodes[0].find_factors()

    def append_right(self, value):
        self.nodes[1] = Node(value)
        self.nodes[1].find_factors()

    def is_prime(self):
        if self.value == 2 or self.value == 3: return True
        if self.value < 2 or self.value % 2 == 0: return False
        if self.value < 9: return True
        if self.value % 3 == 0: return False
        r = int(self.value ** 0.5)
        f = 5
        while f <= r:
            if self.value % f == 0: return False
            if self.value % (f + 2) == 0: return False
            f += 6
        return True

    def find_factors(self):
        random.seed(self.value)
        if self.is_prime():
            return  ## we;re done

        b_ = 2
        b_2 = 2

        factor_list = []

        for i in xrange(2, self.value / 2 + 1):
            if self.value % i == 0:
                factor_list.append(i)

        factor_list.sort()

        nice_factors = (15, 10, 7, 9, 8, 5, 3, 2, 20, 50, 100, 15, 10, 9, 8, 6, 6)
        nic_factors = []
        for i in nice_factors:
            if i in factor_list:
                nic_factors.append(i)

        if len(nic_factors) == 0:
            b_ = factor_list[random.randint(0, len(factor_list) - 1) if len(factor_list) > 1 else 0]
        else:
            b_ = nic_factors[random.randint(0, len(nic_factors) - 1)]

        self.append_left(b_)
        self.append_right(self.value / b_)

    def save_as_pydot(self):
        graph = pydot.Dot(graph_type='graph')
        self._save_as_pydot(None, graph)
        return graph

    def _save_as_pydot(self, parent, graph):
        my_node = pydot.Node("node" + str(id(self)), label=str(self.value), style="filled",
                             fillcolor="white" if not self.is_prime() else "green")
        graph.add_node(my_node)
        if parent is not None:
            graph.add_edge(pydot.Edge(parent, my_node))

        if self.nodes[0] is not None:
            self.nodes[0]._save_as_pydot(my_node, graph)

        if self.nodes[1] is not None:
            self.nodes[1]._save_as_pydot(my_node, graph)

    def prime_factors(self):
        factors = []
        self._prime_factors(factors)
        factors.sort()
        return factors

    def _prime_factors(self, list_):
        if self.is_prime():
            list_.append(self.value)
        else:
            if self.nodes[0] is not None:
                self.nodes[0]._prime_factors(list_)

            if self.nodes[1] is not None:
                self.nodes[1]._prime_factors(list_)


class UniqueInt:
    def __init__(self, num, pos):
        self.num = num
        self.pos = pos

    @classmethod
    def from_list(cls, list_):
        counts = {}
        new_list = []
        for i in list_:
            if i not in counts:
                new_list.append(UniqueInt(i, 0))
                counts[i] = 1
            else:
                new_list.append(UniqueInt(i, counts[i]))
                counts[i] += 1
        return new_list

    def __str__(self):
        return "{}".format(self.num)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if other.num == self.num and other.pos == self.pos:
            return True
        return False

    def __hash__(self):
        return hash(self.num) ^ hash(self.pos)

    def __cmp__(self, other):
        return cmp(self.num, other.num)

    def __int__(self):
        return self.num


fignum_ab = 0

im_font = ImageFont.truetype("OpenSans-Regular.ttf", 15)


def multiline_text_size(text):
    w = 0
    h = 0
    lines = text.split("\n")
    for line in lines:
        lw, lh = im_font.getsize(line)
        h += lh + 10
        w = max(w, lw)
    return w, h


def gen_text_image(text):
    image_size = list(multiline_text_size(text))
    image_size[0] += 20
    image_size[1] += 20

    im = Image.new('RGB', image_size, (255, 255, 255))
    d = ImageDraw.Draw(im)

    d.multiline_text((10, 10), text, font=im_font, fill=(0, 0, 0), spacing=10)
    return im


def stitch_images(img1, img2, img3, im4, header, gfacs):
    im1 = Image.open(img1)
    im2 = Image.open(img2)
    im3 = Image.open(img3)

    width1, h1 = im1.size
    width2, h2 = im2.size

    width_1 = width1 + width2
    width_2, h3 = im3.size

    width4, h4 = im4.size

    width5, h5 = header.size
    width6, h6 = gfacs.size

    width = max(width_1, width_2, width4, width5, width6)
    height = h5 + max(h1, h2) + h3 + h4 + h6

    tree_size = width1 + width2
    tree_offset = max(0, width / 2 - tree_size / 2)

    venn_size = width_2
    venn_offset = max(0, width / 2 - venn_size / 2)

    text_size = width4
    text_offset = max(0, width - text_size)

    header_offset = max(0, width / 2 - width5 / 2)
    gfac_offset = max(0, width / 2 - width6 / 2)

    result = Image.new('RGB', (width, height), (255, 255, 255))
    result.paste(im=header, box=(header_offset, 0))
    result.paste(im=im1, box=(tree_offset, h5))
    result.paste(im=im2, box=(tree_offset + width1, h5))
    result.paste(im=gfacs, box=(gfac_offset, h5 + max(h1, h2)))
    result.paste(im=im3, box=(venn_offset, max(h1, h2) + h5 + h6))
    result.paste(im=im4, box=(text_offset, max(h1, h2) + h3 + h5 + h6))

    im4.save("blablab.png")
    return result


print "Syntax: "
print "<command-letter><arg1>,<arg2>..."
print "Type 'q' to quit"
print
print "=== Valid Commands ==="
print "o - Output a factor tree - takes 1 argument, the number to tree"
print "i - Is this number prime - takes 1 argument, the number to test"
print "f - Output the prime factors - takes 1 argument, the number to factor"
print "v - Create a venn diagram of prime factors - takes 2 arguments, the numbers to venn"
print "p - Create a full image with trees, venn-diagram, cf and cm - takes 3 arguments, the two numbers to use, and "
print "                                                              the amount of cfs and cms"

if __name__ == "__main__":
    last_input = raw_input("> ")
    f = False
    while last_input != "q":
        if f:
            last_input = raw_input("> ")
        f = True
        if last_input == "":
            continue
        if last_input[0] == "o":
            try:
                a = Node(int(last_input[1:]))
            except ValueError:
                print "Invalid number: {}".format(last_input[1:])
                continue
            b = a.save_as_pydot()
            b.write_png(str(a.value) + "_tree.png")
        elif last_input[0] == "i":
            try:
                a = Node(int(last_input[1:]))
            except ValueError:
                print "Invalid number: {}".format(last_input[1:])
                continue
            print a.is_prime()
        elif last_input[0] == "f":
            try:
                a = Node(int(last_input[1:]))
            except ValueError:
                print "Invalid number: {}".format(last_input[1:])
                continue
            print a.prime_factors()
        elif last_input[0] == "v":
            try:
                gin = [int(x) for x in last_input[1:].split(',')]
            except ValueError:
                print "Invalid number"
                continue
            if len(gin) != 2:
                print "Wrong number of arguments, expected 2, got {}".format(len(gin))
                continue
            a = Node(gin[0])
            b = Node(gin[1])
            d = a.prime_factors()
            e = b.prime_factors()

            f = set(UniqueInt.from_list(d))
            g = set(UniqueInt.from_list(e))

            h = f - g
            i = g - f
            j = f & g

            k = " ".join([str(x) for x in h])
            l = " ".join([str(x) for x in i])
            m = " ".join([str(x) for x in j])

            plt.figure(fignum_ab + 1)
            fignum_ab += 1

            v = venn2((4, 4, 4), set_labels=[str(a.value), str(b.value)])
            v.get_label_by_id('10').set_text(k)
            v.get_label_by_id('01').set_text(l)
            v.get_label_by_id('11').set_text(m)

            plt.savefig(str(a.value) + "-" + str(b.value) + "_venn.png")
        elif last_input[0] == "p":
            try:
                gin = [int(x) for x in last_input[1:].split(',')]
            except ValueError:
                print "Invalid number"
                continue
            if len(gin) != 3:
                print "Wrong number of arguments, expected 3, got {}".format(len(gin))
                continue

            a = Node(gin[0])
            b = a.save_as_pydot()
            b.write_png(str(a.value) + "tree.png")

            b = Node(gin[1])
            c = b.save_as_pydot()
            c.write_png(str(b.value) + "tree.png")

            d = a.prime_factors()
            e = b.prime_factors()

            f = set(UniqueInt.from_list(d))
            g = set(UniqueInt.from_list(e))

            h = f - g
            i = g - f
            j = f & g

            k = " ".join([str(x) for x in h])
            l = " ".join([str(x) for x in i])
            m = " ".join([str(x) for x in j])

            plt.figure(fignum_ab + 1)
            fignum_ab += 1

            v = venn2((4, 4, 4), set_labels=[str(a.value), str(b.value)])
            v.get_label_by_id('10').set_text(k)
            v.get_label_by_id('01').set_text(l)
            v.get_label_by_id('11').set_text(m)

            plt.savefig(str(a.value) + "-" + str(b.value) + "venn.png")

            lcm_set = [int(x) for x in h | i | j]
            lcm = reduce(lambda x, y: x * y, lcm_set)
            cms = [lcm]
            left = gin[2] - 1
            at = 2
            while left > 0:
                cms.append(lcm * at)
                at += 1
                left -= 1

            cf_set = [int(x) for x in j]
            gcf = reduce(lambda x, y: x * y, cf_set, 1)
            cfs = [(1, [1]), (gcf, cf_set)]
            for combl in xrange(1, len(cf_set)):
                for subset in itertools.combinations(cf_set, combl):
                    if (reduce(lambda x, y: x * y, subset), subset) in cfs:
                        continue
                    cfs.append((reduce(lambda x, y: x * y, subset), subset))

            cfs_human = ["{} = {}".format(x, " x ".join([str(x) for x in y])) for x, y in cfs]
            if not len(cfs_human) < gin[2]:
                cfs_human = cfs_human[:gin[2]]

            text = ""
            text += "LCM: {} = {}\n".format(lcm, " x ".join(str(x) for x in lcm_set))
            text += "CM: {}\n".format(", ".join(str(x) for x in cms))
            text += "GCF: {}\n".format(gcf)
            text += "CF: {}".format(", ".join(str(x) for x in cfs_human))

            st = stitch_images(str(a.value) + "tree.png", str(b.value) + "tree.png",
                               str(a.value) + "-" + str(b.value) + "venn.png",
                               gen_text_image(text), gen_text_image("GCF and LCM of {} and {}".format(
                    a.value, b.value
                )), gen_text_image("{} = {}\n{} = {}".format(
                    a.value, " x ".join(str(x) for x in d), b.value, " x ".join(str(x) for x in e)
                )))

            st.save(str(a.value) + "-" + str(b.value) + "venntree.png")

            [os.remove(x) for x in
             str(a.value) + "tree.png", str(b.value) + "tree.png", str(a.value) + "-" + str(b.value) + "venn.png"]

        last_input = raw_input("> ")
        f = False
