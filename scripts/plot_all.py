"""Plot many graphs."""

import os
import subprocess

def has_extension(filename, extension):

    name, ext = os.path.splitext(filename)

    return ext == extension

def merge_plot_lines(path):

    all_files = os.listdir(path)

    def is_txt(filename):
        return has_extension(filename, '.txt')

    for fn in filter(is_txt, all_files):
        l_ext = len('_pline.txt')
        stem = fn[:-l_ext]
        print stem

def plot_many_graphs(path):

    all_files = os.listdir(path)

    def is_txt(filename):
        return has_extension(filename, '.txt')

    for fn in filter(is_txt, all_files):
        l_ext = len('_pline.txt')
        stem = fn[:-l_ext]
        output_fn = stem + '_plot.png'
        fq_fn = os.path.join(path, fn)
        fq_output_fn = os.path.join(path, output_fn)

        command = ['Rscript', 'analysis/plot-line.R', fq_fn, fq_output_fn]

        subprocess.call(command)

def main():
    #plot_many_graphs('output')    
    merge_plot_lines('output')

if __name__ == "__main__":
    main()
