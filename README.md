## Project Overview

**MalClass** is a web-based application built with Flask for detecting and classifying suspicious binary files as malware. The system uses a computer vision-based approach with a deep learning model trained on the [MaleVis](https://web.cs.hacettepe.edu.tr/~selman/malevis/) dataset.

The machine learning model used in this system achieves an accuracy of approximately **86.91%**, trained on the MaleVis dataset which consists of 9,100 samples from 25 malware families. Since the dataset only includes a limited number of known families, the system may misclassify files belonging to unknown or novel malware types.

**IMPORTANT**

The file model.tflite is NOT included in this project due to its large size. You can contact me via email: aljauzir@gmail.com or:
1. Train your own CNN model using the MaleVis dataset
2. Export the model to .tflite format using TensorFlow Lite

## Tech Stacks
- Flask (backend server)
- HTML, CSS, JavaScript (static frontend)
- TensorFlow Lite (.tflite model)
- [bin2png](https://github.com/esultanik/bin2png) for binary visualization
- Bootstrap 5 for responsive UI design

## Initialization
### 1. Clone the Repository
```sh
git clone https://github.com/aljauzr/malclass-app.git
cd malclass-app
```
### 2. Create a virtual environment
Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```
Windows:
```sh
python -m venv venv
venv/Scripts/activate
```
### 3. Install the dependencies
```sh
python3 install -r requirements.txt // Change python3 to python if you use Windows
```
### 4. Run the application
```sh
python3 app.py // Change python3 to python if you use Windows
```

## Supported Malware Families
Because of the limitations of the dataset that was used to train the model, it can only detects 25 malware families, which are:
- Adposhel
- Agent
- Allaple
- Amonetize
- Androm
- Autorun
- BrowseFox
- Dinwod
- Elex
- Expiro
- Fasong
- HackKMS
- Hlux
- Injector
- InstallCore
- MultiPlug
- Neoreklami
- Neshta
- Regrun
- Sality
- Snarasite
- Stantinko
- VBA
- VBKrypt
- Vilsel

## Contact
- 📧 Email: aljauzir@gmail.com
- 💼 LinkedIn: [Al Jauzi Abdurrohman](https://linkedin.com/in/aljauzr)
