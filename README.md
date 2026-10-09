# ELCFace

A Python-based face recognition system for a smart voting workflow. The project captures a person's face samples, stores them locally, and then uses a K-Nearest Neighbors (KNN) classifier to recognize the registered individual and allow a vote to be cast through the keyboard.

This project is designed for local, in-person use and stores voter identity and vote records in local files rather than a database.

## Project Overview

The application has two main stages:

1. Face registration: run `add_faces.py` to capture a face, collect samples, and save them for later recognition.
2. Voting system: run `test.py` to recognize the face, detect whether the person has already voted, and record a vote to `Votes.csv`.

The project uses OpenCV for camera access and face detection, and `scikit-learn` to train a simple KNN model based on the captured face data.

## Key Features

- Face registration using a webcam
- Automatic capture of 100 face samples per user
- Local storage of face data and user names in the `data/` folder
- Face recognition through a KNN classifier
- Vote recording in a CSV file (`Votes.csv`)
- Duplicate-vote prevention based on the recognized name
- Audio feedback using Windows Speech API (`SAPI.SpVoice`)
- Keyboard-based vote input: `1`, `2`, `3`, `4`

## Technologies Used

- Python 3
- OpenCV (`opencv-python`)
- NumPy
- scikit-learn
- `pywin32` for Windows COM automation
- CSV-based local storage
- Windows Speech API for voice prompts

## Project Structure

```text
ELCFace/
├── add_faces.py             # Registers a face and saves data to the data folder
├── test.py                  # Main voting system using face recognition
├── background.png           # Background image for the voting interface
├── requirements.txt         # Python dependencies
├── Votes.csv                # Generated at runtime; stores vote records
├── data/
│   ├── faces_data.pkl       # Serialized face feature data
│   └── names.pkl            # Serialized registered names
├── .git/                    # Git metadata
└── README.md                # Project documentation
```

## Prerequisites

Before running the project, make sure the following are available:

- Python 3.8 or newer
- Windows operating system (required because the application uses `pywin32` and Windows SAPI speech)
- Webcam connected to the system
- Speaker or audio output for speech prompts
- A terminal or command prompt with access to Python

## Installation

1. Clone or download the project to your local machine.
2. Open a terminal in the project root.
3. Create and activate a virtual environment if desired.
4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Environment Configuration

No environment variables are required for this project.

The application stores generated data locally in the project folder:

- `data/names.pkl`
- `data/faces_data.pkl`
- `Votes.csv`

These files are created automatically during normal use.

## Running the Project

### 1) Register a face

Run:

```bash
python add_faces.py
```

When the script starts:

- it checks whether the `data/` folder exists and creates it if necessary
- opens the webcam
- detects faces in the live frame
- captures up to 100 samples
- prompts for an "Aadhar number" as the label
- saves the face samples and labels to the `data/` folder

The script stores the data as:

- `data/names.pkl`
- `data/faces_data.pkl`

### 2) Launch the voting system

After at least one user has been registered, run:

```bash
python test.py
```

The voting application will:

- load the trained face data
- create a KNN classifier
- start the webcam
- detect and recognize faces
- display the recognized identity on the video output
- check whether that identity has already voted
- let the user vote using the keyboard with the mapping below

### Vote mapping

| Key   | Party    |
| ----- | -------- |
| `1` | BJP      |
| `2` | CONGRESS |
| `3` | AAP      |
| `4` | NOTA     |

When a valid key is pressed, the application records the vote in `Votes.csv` with the following columns:

- `NAME`
- `VOTE`
- `DATE`
- `TIME`

The script also speaks confirmation messages using Windows speech synthesis.

## Usage Notes

- This project is intended for a local, single-device setup.
- It does not use a remote database or authentication backend.
- It relies on the webcam and local file storage.
- Each recognized name is treated as a voter identity, and duplicate votes are prevented by checking the `Votes.csv` file.
- The program exits after recording one vote for the recognized user in the current session.

## Screenshots and Demo

No screenshots, demo videos, or deployment links were found in the repository.

## Main Entry Points

- `add_faces.py` — data collection and registration
- `test.py` — recognition and voting workflow

## Known Limitations

- Works best on Windows because of `win32com.client` and SAPI voice features.
- Face recognition accuracy depends on lighting, camera quality, and sample quality.
- The voting system is not intended for production-level election infrastructure.
- Data is stored in local pickle/CSV files instead of a secure database or encrypted storage system.

## Future Improvements

Potential enhancements for a more robust version of the project include:

- switching from a local CSV file to a proper database
- adding user authentication or validation before voting
- improving recognition accuracy with better face-recognition models
- adding a graphical UI for easier interaction
- securing data storage and handling duplicate or invalid votes more strictly
- adding tests and validation for the face-registration pipeline

## Contributing

Contributions are welcome if you want to improve the project, especially around accuracy, reliability, and usability.

To contribute:

1. Fork or clone the repository.
2. Create a feature branch.
3. Make your improvements.
4. Run the relevant validation locally.
5. Submit a pull request with a clear summary of your changes.

## License

No explicit license file was found in the project repository. If this project is intended for public reuse, add an appropriate open-source license before distribution.

## Summary

`ELCFace` is a local face-recognition voting prototype that registers a person's face and then recognizes them to allow voting in a small, keyboard-driven election flow. It is a practical demonstration project built with Python, OpenCV, and a KNN-based recognition approach.
