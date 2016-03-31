"""Plot many graphs."""

import os
import subprocess

def has_extension(filename, extension):

    name, ext = os.path.splitext(filename)

    return ext == extension

def extract_intensity_sequence(filename):
    with open(filename) as f:
        lines = f.readlines()

    return [l.split(',')[1].strip() for l in lines]

def merge_plot_lines(path):

    all_files = os.listdir(path)

    def is_txt(filename):
        return has_extension(filename, '.txt')

    all_sequences = {}

    for fn in filter(is_txt, all_files):
        l_ext = len('_pline.txt')
        stem = fn[:-l_ext]
        fq_fn = os.path.join(path, fn)
        # Position 0 is the header
        all_sequences[stem] = extract_intensity_sequence(fq_fn)[1:]

    genotypes = sorted(all_sequences.keys())

    header_line = 'dist,' + ','.join(genotypes) + '\n'

    distances = range(len(all_sequences.values()[0]))
    ordered_sequences = [[str(d) for d in distances]] + [all_sequences[g] for g in genotypes]
    by_time_point = zip(*ordered_sequences)

    def to_line(tp):
        return ','.join(tp) + '\n'

    with open('output/aggregated.csv', 'w') as f:
        f.write(header_line)
        f.write(''.join(to_line(tp) for tp in by_time_point))


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
