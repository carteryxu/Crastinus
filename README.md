# Crastinus
A painful and effective focus program. 

Crastinus is an innovative focus tool that keeps you focused. Utilizing computer vision and classic conditioning concepts, Crastinus keeps you on task by feeding you negative stimuli when your focus shifts.

### Features
---
- Gaze Direction Detection: Utilizes dlib + facial landmarks to determine the your gaze direction in real-time.
- Customizable Focus Zones: Select which gaze directions are considered "focused" (e.g., center, up, down).
- Customizable Negative Stimulus: When the your gaze leaves the designated focus zone, the Crastinus displays a custom image and plays a custom sound to deter you from procrastination

### Requirements
---
- Python 3.x
- OpenCV (cv2)
- dlib
- numpy
- pygame
- PyQt5

### Installation
---
1. Clone the repository:
   ```
    git clone https://github.com/carteryxu/Crastinus.git
    cd Crastinus
   ```
2. Install required packages:
   ```
   pip3 install opencv-python dlib numpy pygame PyQt5
   ```
3. Download shape predictor data:
   - Download `shape_predictor_68_face_landmarks.dat`:
   - https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat
   - Place it in the project root directory.
     
4. (Optional) Download default stimuli:
   - Default stimuli downloads:
   - https://github.com/carteryxu/Crastinus/blob/main/default_files/meekmillfocus.jpg
   - https://github.com/carteryxu/Crastinus/blob/main/default_files/metal%20pipe%20falling%20sound%20effect.wav
   - Place in default_files folder

### Usage
---
1. Run the main script:
   `python main.py `
2. Follow the on-screen instructions to:
   - Select allowed gaze directions
   - Upload custom image and sound stimuli
   - Start focusing!
3. To exit the program, press the 'Esc' key

## Calibration
---
Proper calibration is crucial for Crastinus to accurately detect your gaze direction. Follow these guidelines for optimal performance:

1. Lighting: Ensure you are in an evenly lit area. Avoid strong backlighting or directional light sources that may cast shadows on your face.
2. Camera Position: The current model is calibrated for a laptop camera in a normal sitting position. Your face should be fully visible and centered in the camera frame. Maintain a normal working distance from your camera. 
3. Custom Calibration: If you need to adjust the gaze detection for your specific setup, you can calibrate the model yourself:
   1. Open the `main.py` file in a text editor.
   2. Locate the following line (it should be commented out):
   ```
   # cv2.putText(frame, "Gaze Ratio : " + str(gaze_ratio), (50, 100), font, 2, (0, 0, 255), 2)
   ```
   3. Uncomment this line by removing the # at the beginning.
   4. Run the program and observe the Gaze Ratio values printed on the screen as you look in different directions.
   5. Based your values, adjust the gaze direction thresholds in the following code block:
   ```
   if gaze_ratio < 1:
    gaze_direction = "RIGHT"
   elif 1 <= gaze_ratio < 1.3:
       gaze_direction = "UP"
   elif 1.3 <= gaze_ratio < 1.565:
       gaze_direction = "CENTER"
   elif 1.7 <= gaze_ratio < 2.5:
       gaze_direction = "DOWN"
   else:
       gaze_direction = "LEFT"
    ```
   6. Modify the threshold values to match your observed gaze ratios for each direction.
