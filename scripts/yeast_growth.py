"""Yeast growth analysis."""

import math
import argparse

import numpy as np

from skimage.transform import (
    hough_circle,
    downscale_local_mean
)

from skimage.draw import (
    circle_perimeter,
    line
)

from skimage.measure import profile_line


from jicbioimage.core.image import Image
from jicbioimage.transform import (
    find_edges_sobel,
    smooth_gaussian,
    threshold_otsu
)
from jicbioimage.illustrate import AnnotatedImage

def find_n_best_hough_circles(radii, hough_res, n):
    """Given the radii and hough accumulators for those radii, find the n
    accumulators with the best circles, returning the centers and radii of
    each of those circles in the form (x1, y1, r1), (x2, y2, r2), ...."""

    n_radii = len(radii)

    max_by_radii = [(np.max(hough_res[r,:,:]), r) for r in range(n_radii)]
    max_by_radii.sort(reverse=True)

    best_scores = max_by_radii[:2]

    def flatten_where_result(where_result):
        return [e[0] for e in where_result]

    circles = []
    for score, index in best_scores:
        x, y = flatten_where_result(np.where(hough_res[index,:,:]==score))
        r = radii[index]
        circles.append((x, y, r))

    return circles

def record_line_profile(image, line_start, line_end, filename):

    pline = profile_line(image, line_start, line_end)

    print analyse_line_profile(pline)

    enumerated = list(enumerate(pline))

    #print np.median(pline[100:-100])

    with open(filename, 'w') as f:
        f.write('position,intensity\n')
        values_string = '\n'.join('{},{}'.format(*v) for v in enumerated)
        f.write(values_string)


def find_line_through_point(center, theta, length):
    """Find the coordinates of the start and end of a line passing through the 
    point center, at an angle theta to the x coordinate, extending a distance
    length from the center."""

    r = length
    cx, cy = center

    xo = int(r * math.sin(theta))
    yo = int(r * math.cos(theta))

    line_start = cx, cy
    line_end = cx + xo, cy + yo

    return line_start, line_end

def quantify_yeast_growth(input_filename):

    image = Image.from_file(input_filename)

    blue_channel = image[:,:,2]

    #smoothed = smooth_gaussian(blue_channel.astype(np.float), sigma=20)
    #edges = find_edges_sobel(smoothed)

    #circlet = edges[500:2500, 1000:3000]

    # with open('circlet.png', 'wb') as f:
    #     f.write(circlet.view(Image).png())



    #downscaled = downscale_local_mean(blue_channel, (4, 4))
    downscaled = downscale_local_mean(blue_channel, (2, 2))

    #downscaled = blue_channel

    smoothed = smooth_gaussian(downscaled.astype(np.float), sigma=5)
    edges = find_edges_sobel(smoothed)
    thresh = threshold_otsu(edges)

    hmm = 170, 190
    hough_radii = np.arange(140, 170, 2)
    hough_res = hough_circle(thresh, hough_radii)

    circles = find_n_best_hough_circles(hough_radii, hough_res, 2)
    circle = circles[0]

    # for r in range(10):
    #     hplane = hough_res[r,:,:]
    #     mval = np.max(hplane)
    #     print hough_radii[r], mval, np.where(hplane == mval)

    print hough_res.shape

    circle_coords = circle_perimeter(*circle)

    annotation = AnnotatedImage.from_grayscale(downscaled)

    annotation[circle_coords] = 0, 255, 0

    x, y, r = circle
    center = (x, y)

    lines = []
    range_start = -math.pi/4
    range_end = math.pi/4
    line_length = 380#475

    print 'SHAPE', downscaled.shape
    for theta in np.linspace(range_start, range_end, 200):
        line_start, line_end = find_line_through_point(center, theta, line_length)

        pline = profile_line(smoothed, line_start, line_end)
        annotation_line = line(*(line_start + line_end))

        annotation[annotation_line] = 0, 255, 255

        lines.append(pline[:line_length-1])
        #print len(pline)

    lines_as_matrix = np.stack(lines)
    average_lines = np.median(lines_as_matrix, axis=0)

    enumerated = list(enumerate(average_lines))
    filename = '/output/pline.txt'

    with open(filename, 'w') as f:
        f.write('position,intensity\n')
        values_string = '\n'.join('{},{}'.format(*v) for v in enumerated)
        f.write(values_string)

    with open('annotation.png', 'wb') as f:
        f.write(annotation.png())



def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('input_filename')
    args = parser.parse_args()

    quantify_yeast_growth(args.input_filename)

if __name__ == '__main__':
    main()