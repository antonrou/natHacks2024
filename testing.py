import dataTransform
from matrix_test import random_matrix

#data_stream = ogData_streaming.data_stream()
filtered_data = dataTransform.data_transform(random_matrix())

#for key in filtered_data:
print(filtered_data['delta'])

# test with a sample matrix

# dataTransform.data_transform(data_stream)