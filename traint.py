import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

try:
    # Load data
    data_dict = pickle.load(open('./data.pickle', 'rb'))
except Exception as e:
    print("Error loading data:", e)
    exit()

try:
    # Convert data to numpy arrays
    data = np.asarray(data_dict['data'])
    labels = np.asarray(data_dict['labels'])
except Exception as e:
    print("Error converting data to numpy arrays:", e)
    exit()

try:
    # Split data into train and test sets
    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.4, shuffle=True, stratify=labels)
except Exception as e:
    print("Error splitting data into train and test sets:", e)
    exit()

try:
    # Train the model
    model = RandomForestClassifier()
    model.fit(x_train, y_train)
except Exception as e:
    print("Error training the model:", e)
    exit()

try:
    # Make predictions
    y_predict = model.predict(x_test)
except Exception as e:
    print("Error making predictions:", e)
    exit()

try:
    # Calculate accuracy score
    score = accuracy_score(y_predict, y_test)
except Exception as e:
    print("Error calculating accuracy score:", e)
    exit()

print('{}% of samples were classified correctly!'.format(score * 100))

try:
    # Save the model
    f = open('model.p', 'wb')
    pickle.dump({'model': model}, f)
    f.close()
except Exception as e:
    print("Error saving the model:", e)