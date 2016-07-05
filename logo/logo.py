from os import makedirs
from os.path import join, isdir
from subprocess import check_output


def make_dir(path):
    if not isdir(path):
        makedirs(path)

def set_background(image_filename, color):
    command = 'convert {0} -background "{1}" -flatten {0}'.format(image_filename, color)
    print(command)
    check_output(command, shell=True)


def convert_to_bitmap(vector_filename, out_filename, size):
    width, height = size
    command = 'inkscape -z -e {1} -w {2} -h {3} {0}'.format(vector_filename, out_filename, width, height)
    print(command)
    check_output(command, shell=True)


def ios(vector_filename, output_path, output_base_filename, sizes, background=None):
    for size, multipliers in sizes.iteritems():
        if type(size) == tuple:
            width, height = size
        else:
            width = size
            height = size
        for multiplier in multipliers:
            m_width = width * multiplier
            m_height = height * multiplier
            if width == height:
                output_filename = '{0}-{1}@{2}x.png'.format(output_base_filename, width, multiplier)
            else:
                output_filename = '{0}-{1}-{2}@{3}x.png'.format(output_base_filename, width, height, multiplier)
            make_dir(output_path)
            output_filepath = join(output_path, output_filename)
            convert_to_bitmap(vector_filename, output_filepath, (m_width, m_height))
            if background:
                set_background(output_filepath, background)


if __name__=='__main__':
    app_icon_sizes = {
        60: [2, 3],
        76: [1, 2],
        83.5: [2]
    }

    ios('logo_material.svg', 'generated/AppIcon.appiconset','syncloud', app_icon_sizes, '#FFFFFF')

    ios('logo_material.svg', 'generated/syncloud_logo', 'syncloud_log', {667: [1]})