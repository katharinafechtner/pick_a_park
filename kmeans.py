# Analyze image
import matplotlib.pyplot as plt
import matplotlib.image as img
from scipy.cluster.vq import whiten
from sklearn.cluster import KMeans
import numpy as np

'''
https://www.geeksforgeeks.org/extract-dominant-colors-of-an-image-using-python/
https://medium.com/analytics-vidhya/color-separation-in-an-image-using-kmeans-clustering-using-python-f994fa398454
--> used a mix of both tutorials. first link uses cv2 which doed not work on windows
allows finding of optimal cluster number (elbow)
--> second link does not scale colors with standard deviation as recommended for kmeans
and also requires cluster number as input
'''

# Standard deviation of list
# Using sum() + list comprehension
def std_dev(data):
    mean = sum(data) / len(data)
    variance = sum([((x - mean) ** 2) for x in data]) / len(data)
    res = variance ** 0.5
    return res


def Kmeans(dirname):
    # Read image
    pic_path = dirname + "\\static\\screenshots\\screenshot.jpg"
    pic = img.imread(pic_path)

    # Store shape to reassemble later
    M_shape = pic.shape[0]
    N_shape = pic.shape[1]

    # Store RGB values of all pixels in lists r, g and b
    r, g, b = ([] for i in range(3))
    count = 1
    # Scaling the values
    for rows in pic:
        for r_temp, g_temp, b_temp in rows:
            r.append(r_temp)
            g.append(g_temp)
            b.append(b_temp)

    # Calculate standard deviation
    r_std = std_dev(r)
    g_std = std_dev(g)
    b_std = std_dev(b)

    # Scale colors        
    scaled_r = whiten(r)
    scaled_g = whiten(g)
    scaled_b = whiten(b)

    r_ = scaled_r * r_std
    g_ = scaled_g * g_std
    b_ = scaled_b * b_std

    # Put RGB values back together
    RGB_array = np.column_stack([r_, g_, b_]).reshape(M_shape*N_shape, 3)

    # Run kmeans learning process
    kmeans = KMeans(n_clusters=5)
    s = kmeans.fit(RGB_array)

    # Determine the labels for each RGB pixel intensities
    labels=kmeans.labels_
    labels=list(labels)

    # Determine centroids of clusters
    centroid = kmeans.cluster_centers_

    # Calculate percentages that each cluster constitutes
    percent = []
    for i in range(len(centroid)):
        j = labels.count(i)
        j = j / (len(labels))
        percent.append(j)

    # Plot pie chart
    chart_name = dirname + "\\static\\screenshots\\kmeans.jpg"

    # create a figure and set different background
    fig = plt.figure()
    fig.patch.set_facecolor('lightgrey')

    plt.pie(percent, colors=np.array(centroid/255), labels=np.arange(len(centroid)))

    # Save figure
    plt.savefig(chart_name)
    #plt.show()
