# Importing packages
from src.components.detect_drift import DetectDataDrift

# Running the drift detection process
if __name__ == '__main__':
    drift_detector = DetectDataDrift()
    drift_detector.run_drift_detection()