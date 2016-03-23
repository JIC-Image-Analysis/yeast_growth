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

def record_line_profile(filename, pline):

    enumerated = list(enumerate(pline))

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

def fit_central_circle(image, radius_lower_bound=170, radius_upper_bound=190):
    """Find the centre and radius of the central circle in image. Analysis is
    restrictied the given bounds for the radius of the circle."""

    smoothed = smooth_gaussian(image.astype(np.float), sigma=5)
    edges = find_edges_sobel(smoothed)
    thresh = threshold_otsu(edges)

    hmm = 170, 190
    hough_radii = np.arange(140, 170, 2)
    hough_res = hough_circle(thresh, hough_radii)

    circles = find_n_best_hough_circles(hough_radii, hough_res, 1)
    circle = circles[0]

    return circle

def load_and_downscale(input_filename):
    """Load the image, covert to grayscale and downscale as needed."""

    image = Image.from_file(input_filename)
    blue_channel = image[:,:,2]
    downscaled = downscale_local_mean(blue_channel, (2, 2))

    return downscaled

def find_mean_profile_line(image, annotation, center, theta_start, theta_end, length):

    lines = []

    for theta in np.linspace(theta_start, theta_end, 200):
        line_start, line_end = find_line_through_point(center, theta, length)

        pline = profile_line(image, line_start, line_end)
        annotation_line = line(*(line_start + line_end))

        annotation[annotation_line] = 0, 255, 255

        lines.append(pline[:length-1])

    lines_as_matrix = np.stack(lines)

    average_lines = np.mean(lines_as_matrix, axis=0)

    return average_lines

def quantify_yeast_growth(input_filename, annotation_filename, 
                            profile_filename):
    

    downscaled = load_and_downscale(input_filename)
    annotation = AnnotatedImage.from_grayscale(downscaled)

    circle = fit_central_circle(downscaled)

    circle_coords = circle_perimeter(*circle)
    annotation[circle_coords] = 0, 255, 0

    x, y, r = circle
    center = (x, y)

    mean_profile_line = find_mean_profile_line(downscaled, annotation,
                                center, -math.pi/4, math.pi/4, 380)


    record_line_profile(profile_filename, mean_profile_line)

    with open(annotation_filename, 'wb') as f:
        f.write(annotation.png())

def generate_arguments_and_quantify_yeast(input_filename):

    annotation_filename = '/output/annotation.png'
    profile_filename = '/output/pline.txt'

    quantify_yeast_growth(input_filename, annotation_filename, 
                            profile_filename)


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('input_filename')
    args = parser.parse_args()

    generate_arguments_and_quantify_yeast(args.input_filename)


if __name__ == '__main__':
    main()