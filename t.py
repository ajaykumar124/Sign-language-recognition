import pickle
import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Load the model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize Hands module
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.6, max_num_hands=1)

# Define label dictionary
labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
               10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S',
               19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}

# Initialize variables for smoothing predictions
buffer_size = 10  # Number of frames to buffer predictions
prediction_buffer = []
last_prediction = ""  # Initialize last_prediction variable
formed_word = ""  # Initialize formed word

# Function to toggle gesture recognition
def toggle_recognition():
    global recognition_running
    recognition_running = not recognition_running
    if recognition_running:
        update_frame()

# Function to clear the formed word text
def clear_formed_word():
    global formed_word
    formed_word = ""
    word_label.config(text=formed_word)

# Function to update video frame in the GUI
def update_frame():
    global formed_word
    global last_prediction  # Declare last_prediction as global variable
    if recognition_running:
        ret, frame = cap.read()  # Read frame from the video stream

        if ret:
            H, W, _ = frame.shape  # Get frame dimensions
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB
            results = hands.process(frame_rgb)  # Process the frame with MediaPipe Hands

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                               mp_drawing_styles.get_default_hand_landmarks_style(),
                                               mp_drawing_styles.get_default_hand_connections_style())

                    data_aux = []
                    x_ = []
                    y_ = []

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y

                        x_.append(x)
                        y_.append(y)

                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                    x1 = int(min(x_) * W) - 10
                    y1 = int(min(y_) * H) - 10

                    x2 = int(max(x_) * W) - 10
                    y2 = int(max(y_) * H) - 10

                    prediction = model.predict([np.asarray(data_aux)])

                    predicted_character = labels_dict[int(prediction[0])]

                    # Update prediction buffer
                    prediction_buffer.append(predicted_character)
                    if len(prediction_buffer) > buffer_size:
                        prediction_buffer.pop(0)

                    # Smoothed prediction
                    smoothed_prediction = max(set(prediction_buffer), key=prediction_buffer.count)

                    if smoothed_prediction != last_prediction:
                        formed_word += smoothed_prediction
                        last_prediction = smoothed_prediction

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                    cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                                cv2.LINE_AA)

            # Resize frame to fit within a certain width and height while maintaining aspect ratio
            max_width = root.winfo_screenwidth()
            max_height = root.winfo_screenheight()
            frame = resize_frame(frame, max_width, max_height)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))  # Convert frame to ImageTk format
            panel.img = img
            panel.configure(image=img)  # Update the image in the panel

            # Display the formed word
            word_label.config(text=formed_word)

        panel.after(10, update_frame)  # Update frame every 10 milliseconds

def resize_frame(frame, max_width, max_height):
    # Get frame dimensions
    H, W, _ = frame.shape
    
    # Calculate aspect ratio
    aspect_ratio = W / H
    
    # Resize frame to fit within max_width and max_height while maintaining aspect ratio
    if W > H:
        new_width = min(W, max_width)
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = min(H, max_height)
        new_width = int(new_height * aspect_ratio)
    
    return cv2.resize(frame, (new_width, new_height))

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize the GUI
root = tk.Tk()
root.title("Gesture Recognition")
root.geometry("1000x700")  # Set initial window size
root.configure(bg="#222831")  # Set background color

# Load background image
background_image = Image.open("back1.jpg")  # Provide path to your background image
background_image = background_image.resize((1600, 1000), Image.BILINEAR)
background_image = ImageTk.PhotoImage(background_image)

# Display the background image
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place at (0, 0) and cover the entire window

# Create a panel to display video frames
panel = tk.Label(root, bg="#000000")
panel.place(relx=0.5, rely=0.4, anchor="center")  # Center the panel

# Label to display formed word
# Label to display formed word
word_label = tk.Label(root, text="", font=("Arial", 18), bg="#222831", fg="#ffffff", padx=10, pady=2, width=5)

word_label.pack(side=tk.BOTTOM, fill=tk.X)  # Place at bottom with padding

# Start/Stop button
start_stop_button = tk.Button(root, text="Start", command=toggle_recognition, bg="#00adb5", fg="#ffffff", bd=0,
                              padx=20, pady=10, font=("Arial", 16, "bold"))
start_stop_button.place(relx=0.25, rely=0.8, anchor="center")  # Position the button

# Clear button
clear_button = tk.Button(root, text="Clear", command=clear_formed_word, bg="#ff5722", fg="#ffffff", bd=0,
                         padx=20, pady=10, font=("Arial", 16, "bold"))
clear_button.place(relx=0.5, rely=0.8, anchor="center")  # Position the button

# Exit button
exit_button = tk.Button(root, text="Exit", command=root.quit, bg="#ffbd69", fg="#222831", bd=0,
                        padx=20, pady=10, font=("Arial", 16, "bold"))
exit_button.place(relx=0.75, rely=0.8, anchor="center")  # Position the button

# Initialize recognition state
recognition_running = False

# Run the GUI
root.mainloop()

# Release video capture
cap.release()
cv2.destroyAllWindows()