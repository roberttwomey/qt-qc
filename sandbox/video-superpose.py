import cv2
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer


# === Qiskit: Generate Quantum Collapse ===
qc = QuantumCircuit(2, 2)
qc.h([0, 1])             # Superposition
qc.measure([0, 1], [0, 1])

backend = Aer.get_backend('qasm_simulator')
job = backend.run(qc, shots=1)  # 1 shot to simulate single collapse
result = job.result()
counts = result.get_counts()
outcome = list(result.get_counts().keys())[0]  # e.g. '10'
print(f"Measured: {outcome}")

# === File Paths for Videos ===
video_paths = {
    "00": "video-00.mov",
    "01": "video-01.mov",
    "10": "video-10.mov",
    "11": "video-11.mov",
}

# === Load all videos ===
caps = {k: cv2.VideoCapture(video_paths[k]) for k in video_paths}
fps = caps["00"].get(cv2.CAP_PROP_FPS)
frame_count = int(caps["00"].get(cv2.CAP_PROP_FRAME_COUNT))
width = int(caps["00"].get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(caps["00"].get(cv2.CAP_PROP_FRAME_HEIGHT))

# === Create Window ===
cv2.namedWindow("Quantum Video", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Quantum Video", width, height)

# === Loop the sequence until user presses Escape ===
while True:
    # Reset all video captures to the first frame
    for cap in caps.values():
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    collapsed_cap = cv2.VideoCapture(video_paths[outcome])
    
    # === Play through blended superposition ===
    last_blended = None
    for i in range(frame_count):
        frames = []
        for cap in caps.values():
            ret, frame = cap.read()
            if ret:
                frame = frame.astype(np.float32)
                frames.append(frame)
        if len(frames) == 4:
            # Blend all four frames equally
            blended = sum(frames) / 4.0
            blended = np.clip(blended, 0, 255).astype(np.uint8)
            last_blended = blended.copy()
            # Display 'superposition' text for the first second
            if i < int(fps):
                cv2.putText(
                    blended, 'superposition', (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4, cv2.LINE_AA
                )
            cv2.imshow("Quantum Video", blended)
            key = cv2.waitKey(int(1000 / fps)) & 0xFF
            if key == 27:  # Escape key
                for cap in caps.values():
                    cap.release()
                collapsed_cap.release()
                cv2.destroyAllWindows()
                exit()
    
    # === Lerp transition from last superposition to first collapsed frames (dynamic) ===
    transition_frames = 30
    if last_blended is not None:
        last_blended_f = last_blended.astype(np.float32)
        for i in range(transition_frames):
            ret, collapsed_frame = collapsed_cap.read()
            if not ret:
                break
            collapsed_f = collapsed_frame.astype(np.float32)
            alpha = (i + 1) / transition_frames
            frame = (1 - alpha) * last_blended_f + alpha * collapsed_f
            frame = np.clip(frame, 0, 255).astype(np.uint8)
            cv2.imshow("Quantum Video", frame)
            key = cv2.waitKey(int(1000 / fps)) & 0xFF
            if key == 27:
                for cap in caps.values():
                    cap.release()
                collapsed_cap.release()
                cv2.destroyAllWindows()
                exit()
    
    # === Show only collapsed video ===
    collapse_text_frames = int(fps)
    collapse_frame_idx = 0
    collapsed_frames_list = []  # Store collapsed frames for transition back
    while True:
        ret, frame = collapsed_cap.read()
        if not ret:
            break
        # Store for transition back
        collapsed_frames_list.append(frame.copy())
        # Display 'collapse' text for the first second
        if collapse_frame_idx < collapse_text_frames:
            cv2.putText(
                frame, 'collapse', (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4, cv2.LINE_AA
            )
        collapse_frame_idx += 1
        cv2.imshow("Quantum Video", frame)
        key = cv2.waitKey(int(1000 / fps)) & 0xFF
        if key == 27:
            for cap in caps.values():
                cap.release()
            collapsed_cap.release()
            cv2.destroyAllWindows()
            exit()
    collapsed_cap.release()

    # === Lerp transition from collapse back to superposition (dynamic) ===
    # Rewind all input video captures to the start
    for cap in caps.values():
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    # Rewind collapsed video to the start (for dynamic frames)
    collapsed_cap = cv2.VideoCapture(video_paths[outcome])
    transition_frames = 30
    for i in range(transition_frames):
        # Read next collapsed frame
        ret_c, collapsed_frame = collapsed_cap.read()
        # Read next blended superposition frame
        frames = []
        for cap in caps.values():
            ret, frame = cap.read()
            if ret:
                frame = frame.astype(np.float32)
                frames.append(frame)
        if not ret_c or len(frames) != 4:
            break
        blended = sum(frames) / 4.0
        blended = np.clip(blended, 0, 255).astype(np.uint8)
        collapsed_f = collapsed_frame.astype(np.float32)
        alpha = (i + 1) / transition_frames
        frame = (1 - alpha) * collapsed_f + alpha * blended.astype(np.float32)
        frame = np.clip(frame, 0, 255).astype(np.uint8)
        # Optionally, display 'superposition' text for the last few frames
        if i >= transition_frames - int(fps):
            cv2.putText(
                frame, 'superposition', (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4, cv2.LINE_AA
            )
        cv2.imshow("Quantum Video", frame)
        key = cv2.waitKey(int(1000 / fps)) & 0xFF
        if key == 27:
            for cap in caps.values():
                cap.release()
            collapsed_cap.release()
            cv2.destroyAllWindows()
            exit()
    collapsed_cap.release()
