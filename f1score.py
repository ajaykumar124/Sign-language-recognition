import tkinter as tk
from tkinter import ttk
import pickle
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkthemes import ThemedStyle

def load_model(model_file):
    try:
        with open(model_file, 'rb') as file:
            model_dict = pickle.load(file)
            model = model_dict['model']
        return model
    except FileNotFoundError:
        print(f"Model file '{model_file}' not found.")
        exit()

def load_test_data(data_file):
    try:
        with open(data_file, 'rb') as file:
            data_dict = pickle.load(file)
            test_data = np.asarray(data_dict['data'])
            test_labels = np.asarray(data_dict['labels'])
        return test_data, test_labels
    except FileNotFoundError:
        print(f"Data file '{data_file}' not found.")
        exit()

def calculate_metrics(model, test_data, test_labels):
    # Make predictions on the test data
    test_predictions = model.predict(test_data)

    # Calculate metrics
    accuracy = accuracy_score(test_labels, test_predictions) * 100
    precision = precision_score(test_labels, test_predictions, average='macro') * 100
    recall = recall_score(test_labels, test_predictions, average='macro') * 100
    f1 = f1_score(test_labels, test_predictions, average='macro') * 100
    conf_matrix = confusion_matrix(test_labels, test_predictions)

    return accuracy, precision, recall, f1, conf_matrix

def create_gui(accuracy, precision, recall, f1, conf_matrix):
    root = tk.Tk()
    root.title("Model Evaluation")
    root.geometry("800x800")

    # Apply a themed style
    style = ThemedStyle(root)
    style.set_theme("equilux")

    # Header frame
    header_frame = ttk.Frame(root)
    header_frame.pack(pady=10)
    ttk.Label(header_frame, text="Model Evaluation", font=("Helvetica", 20, "bold")).pack()

    # Metrics frame
    metrics_frame = ttk.Frame(root)
    metrics_frame.pack(pady=20)
    ttk.Label(metrics_frame, text=f"Accuracy: {accuracy:.2f}%", font=("Helvetica", 12)).pack(anchor='w')
    ttk.Label(metrics_frame, text=f"Precision: {precision:.2f}%", font=("Helvetica", 12)).pack(anchor='w')
    ttk.Label(metrics_frame, text=f"Recall: {recall:.2f}%", font=("Helvetica", 12)).pack(anchor='w')
    ttk.Label(metrics_frame, text=f"F1 Score: {f1:.2f}%", font=("Helvetica", 12)).pack(anchor='w')

    # Confusion matrix frame
    matrix_frame = ttk.Frame(root)
    matrix_frame.pack(pady=20)
    ttk.Label(matrix_frame, text="Confusion Matrix", font=("Helvetica", 14, "bold")).pack()

    # Display confusion matrix with lighter blue color
    fig, ax = plt.subplots()
    cax = ax.matshow(conf_matrix, cmap=plt.cm.Paired)  # lighter blue colormap
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            ax.text(x=j, y=i, s=conf_matrix[i, j], va='center', ha='center')
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.colorbar(cax)
    plt.title('Confusion Matrix')
    plt.tight_layout()

    # Convert the matplotlib figure to a Tkinter-compatible canvas
    canvas = FigureCanvasTkAgg(fig, master=matrix_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    root.mainloop()

def main():
    # Load the model
    model_file = 'model.p'
    model = load_model(model_file)

    # Load the test data
    data_file = 'data.pickle'
    test_data, test_labels = load_test_data(data_file)

    # Calculate metrics
    accuracy, precision, recall, f1, conf_matrix = calculate_metrics(model, test_data, test_labels)

    # Create and display GUI
    create_gui(accuracy, precision, recall, f1, conf_matrix)

if __name__ == "__main__":
    main()
