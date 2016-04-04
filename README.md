# Yeast Growth Quantification

1. Find the filter disk via a Hough transform (circle finding algorithm) (annotated in green).
2. Find the intensity profile along a number of radii from the center of this disk outwards (annotated in blue).
3. Average these intensity profiles to give a single profile of image intensity versus distance from center of the filter disk.
