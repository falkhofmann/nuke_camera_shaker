import random
import os


def get_output_dir():
    return '../data'


def create_shake(count):
    filename = '{}.txt'.format(str(count).zfill(4))
    filepath = os.path.join(get_output_dir(), filename)
    content = ''
    for each in xrange(10):
        x = random.uniform(-10.0,  10.0)
        y = random.uniform(-11.0, 9.0)
        line = '{} {}\n'.format(x, y)
        content += line
    doc = open(filepath, 'w')
    doc.write(content)


def generate():
    for each in range(1, 110):
        create_shake(each)


if __name__ == '__main__':
    generate()
