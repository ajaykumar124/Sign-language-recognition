# Sign-language-recognition

## Overview

This project is designed to recognize sign language gestures using a machine learning model trained on hand landmarks data. The project consists of a series of scripts for collecting image data, creating datasets, training a machine learning model, and implementing a user interface for sign language recognition. The application uses MediaPipe for hand landmarks detection and a Random Forest classifier for gesture recognition.

## Project Structure

- **collect_images.py**: Script for capturing images of different sign language gestures using a webcam.
- **create_dataset.py**: Script for processing the collected images, extracting hand landmarks, and creating a dataset.
- **train.py**: Script for training the machine learning model using the created dataset.
- **signup.py**: Script for user signup and login using a GUI built with Tkinter.
- **t.py**: Main script for real-time sign language recognition and displaying the results in a GUI.

## Installation
```bash
pip install opencv-python
pip install mediapipe
pip install scikit-learn
pip install matplotlib
pip install Pillow
pip install numpy
```

### Prerequisites

- Python 3.x
- Required Python packages (listed in `requirements.txt`)

### Steps

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Ensure you have a working webcam connected to your system.

## Usage

### Data Collection

1. Run the `collect_images.py` script to start capturing images for each sign language gesture,make sure you have made a folder named as Data.

    ```bash
    python collect_images.py
    ```

2. Follow the on-screen instructions to capture images for each class.

### Dataset Creation

1. Run the `create_dataset.py` script to process the collected images and create a dataset.

    ```bash
    python create_dataset.py
    ```

2. This will generate a `data.pickle` file containing the processed data and labels.

### Model Training

1. Run the `train.py` script to train the machine learning model.

    ```bash
    python train.py
    ```

2. This will generate a `model.p` file containing the trained model.

### User Signup and Login

1. Run the `signup.py` script to start the user interface for signup and login.

    ```bash
    python signup.py
    ```

2. Follow the on-screen instructions to create a new user or login with existing credentials.

### Sign Language Recognition

1. After successful login, the `t.py` script will be launched automatically.
2. The real-time sign language recognition will start, displaying the recognized gestures on the screen.
3. Use the Start/Stop button to control the recognition process, the Clear button to clear the formed word, and the Exit button to close the application.

## Script Details

### collect_images.py

- Captures images using a webcam.
- Creates directories for each class if they do not exist.
- Captures 100 images per class and saves them in the respective directories.

### create_dataset.py

- Processes the captured images to extract hand landmarks using MediaPipe.
- Normalizes the landmarks data and creates a dataset.
- Saves the dataset as a `data.pickle` file.

### train.py

- Loads the dataset from the `data.pickle` file.
- Trains a Random Forest classifier on the dataset.
- Evaluates the model on a test set and prints the accuracy.
- Saves the trained model as a `model.p` file.

### signup.py

- Provides a GUI for user signup and login using Tkinter.
- Stores user credentials in an SQLite database.
- Allows users to login and launches the `t.py` script for sign language recognition upon successful login.

### t.py

- Loads the trained model from the `model.p` file.
- Uses MediaPipe for real-time hand landmarks detection.
- Predicts the sign language gesture and displays it in a GUI.
- Allows users to start/stop the recognition process, clear the formed word, and exit the application.

## Notes

- Ensure that the background image (`back1.jpg`) is placed in the same directory as the scripts.
- The application uses a smoothing technique to improve prediction accuracy by averaging predictions over a buffer of 10 frames.

## Future Work

- Improve the accuracy of the model by collecting more diverse data.
- Implement additional sign language gestures.
- Enhance the user interface with more features and better design.
- Explore the use of more advanced machine learning models and techniques.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for more details.
