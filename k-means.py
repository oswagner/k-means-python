import sys
import random
import math
import matplotlib.pyplot as plt


def organize_data(file_content):
    data_set = []
    lines = file_content.readlines()
    for iris_line_values in lines:
        values = iris_line_values.split(',')
        data_set.append({
            'sepal_length': float(values[0]),
            'sepal_width': float(values[1]),
            'petal_length': float(values[2]),
            'petal_width': float(values[3]),
            'cluster': -1,
        })
    return data_set


def generate_random_centroid(cluster_numbers, data_set):
    centroids = []
    for k in range(0, cluster_numbers):
        random_index_centroid = random.randint(0, len(data_set))
        centroid = dict(data_set[random_index_centroid])
        centroid['cluster'] = k
        centroids.append(centroid)
    return centroids


def evaluate_euclidean_distance(current, centroid):
    current_sepal_length = current['sepal_length']
    current_sepal_width = current['sepal_width']
    current_petal_lenght = current['petal_length']
    current_petal_width = current['petal_width']

    centroid_sepal_length = centroid['sepal_length']
    centroid_sepal_width = centroid['sepal_width']
    centroid_petal_length = centroid['petal_length']
    centroid_petal_width = centroid['petal_width']

    # x1 = [1,1,4]
    # x2 = [10,2,7]
    # # Calculating distance by using math
    # eudistance = math.sqrt(math.pow(x1[0]-x2[0],2) + math.pow(x1[1]-x2[1],2) + math.pow(x1[2]-x2[2],2) )
    # print("eudistance Using math ", eudistance)

    euclidean_distance = math.sqrt(
        math.pow(current_sepal_length - centroid_sepal_length, 2) +
        math.pow(current_sepal_width - centroid_sepal_width, 2) +
        math.pow(current_petal_lenght - centroid_petal_length, 2) +
        math.pow(current_petal_width - centroid_petal_width, 2)
    )
    return euclidean_distance


def cluster_selection(flower, centroids):
    shortest_distance = 100
    for centroid in centroids:
        current_shortest_distance = evaluate_euclidean_distance(
            flower, centroid
        )
        if current_shortest_distance < shortest_distance:
            flower['cluster'] = centroid['cluster']
            shortest_distance = current_shortest_distance


def evaluate_new_centroid(cluster):
    sepal_length = sum(flower['sepal_length'] for flower in cluster)
    sepal_width = sum(flower['sepal_width']for flower in cluster)
    petal_length = sum(flower['petal_length'] for flower in cluster)
    petal_width = sum(flower['petal_width'] for flower in cluster)

    return {
        'sepal_length': (sepal_length / len(cluster)),
        'sepal_width': (sepal_width / len(cluster)),
        'petal_length': (petal_length / len(cluster)),
        'petal_width': (petal_width / len(cluster)),
        'cluster': cluster[0]['cluster'],
    }


def update_centroid(flowers, centroids):
    new_centroids = []
    for centroid in centroids:
        cluster = filter_cluster(flowers, centroid)
        new_centroids.append(evaluate_new_centroid(cluster))

    return new_centroids


def filter_cluster(flowers, centroid):
    return [
        flower for flower in flowers
        if flower['cluster'] == centroid['cluster']
    ]


def configure_plot(data_set):
    for flower in data_set:
        if flower['cluster'] == 0:
            plt.scatter(
                x=flower['sepal_length'],
                y=flower['sepal_width'],
                c='#4E3DB3',
                marker='X'
            )

        if flower['cluster'] == 1:
            plt.scatter(
                x=flower['sepal_length'],
                y=flower['sepal_width'],
                c='#4BB346',
                marker='X'
            )

        if flower['cluster'] == 2:
            plt.scatter(
                x=flower['sepal_length'],
                y=flower['sepal_width'],
                c='#FFC399',
                marker='X'
            )


def main():
    k = int(sys.argv[1])
    max_iterations = int(sys.argv[2])
    file_content = open('iris.data', 'r')

    data_set = organize_data(file_content)

    centroids = generate_random_centroid(k, data_set)

    for _ in range(0, max_iterations):
        for i in range(0, len(data_set)):
            # for i in range(0, 1):
            for flower in data_set:
                cluster_selection(flower, centroids)

        centroids = update_centroid(data_set, centroids)

    print("finished")
    configure_plot(data_set)
    plt.show()


if __name__ == "__main__":
    main()
