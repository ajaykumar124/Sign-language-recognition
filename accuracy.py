import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix

def load_model(model_file):
    try:
        model_dict = pickle.load(open(model_file, 'rb'))
        model = model_dict['model']
        return model
    except FileNotFoundError:
        print(f"Model file '{model_file}' not found.")
        exit()

def load_test_data(data_file):
    try:
        data_dict = pickle.load(open(data_file, 'rb'))
        test_data = np.asarray(data_dict['data'])
        test_labels = np.asarray(data_dict['labels'])
        return test_data, test_labels
    except FileNotFoundError:
        print(f"Data file '{data_file}' not found.")
        exit()

def plot_confusion_matrix(conf_matrix):
    plt.figure(figsize=(10, 8))
    sns.heatmap(conf_matrix, annot=True, cmap="Blues", fmt="d", xticklabels=range(25), yticklabels=range(25))
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.title("Confusion Matrix")
    plt.show()

def main():
    # Load the model
    model_file = 'model.p'
    model = load_model(model_file)

    # Load the test data
    data_file = 'data.pickle'
    test_data, test_labels = load_test_data(data_file)

    # Make predictions on the test data
    test_predictions = model.predict(test_data)

    # Calculate accuracy
    accuracy = accuracy_score(test_labels, test_predictions)
    print('Accuracy:', accuracy * 100, '%')

    # Generate confusion matrix
    conf_matrix = confusion_matrix(test_labels, test_predictions)
    print('Confusion Matrix:')
    print(conf_matrix)

    # Plot confusion matrix
    plot_confusion_matrix(conf_matrix)

if __name__ == "__main__":
    main()
