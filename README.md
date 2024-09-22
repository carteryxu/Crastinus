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
   - https://github.com/carteryxu/Crastinus/blob/main/eye_tracking/meekmillfocus.jpg
   - https://github.com/carteryxu/Crastinus/blob/main/eye_tracking/metal%20pipe%20falling%20sound%20effect.wav

### Usage
---
1. Run the main script:
   `python main.py `
2. Follow the on-screen instructions to:
   - Select allowed gaze directions
   - Upload custom image and sound stimuli
   - Start focusing!
3. To exit the program, press the 'Esc' key
   
