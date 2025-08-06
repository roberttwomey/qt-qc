import cv2
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer


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


transition_frames = 30
play_frames = 120

# === Loop the sequence until user presses Escape ===
while True:
    # === Qiskit: Generate Quantum Collapse (each loop) ===
    qc = QuantumCircuit(2, 2)
    qc.h([0, 1])             # Superposition
    qc.measure([0, 1], [0, 1])
    backend = Aer.get_backend('qasm_simulator')
    job = backend.run(qc, shots=1)  # 1 shot to simulate single collapse
    result = job.result()
    counts = result.get_counts()
    outcome = list(result.get_counts().keys())[0]  # e.g. '10'
    print(f"Measured: {outcome}")

    # Reset all video captures to the first frame
    for cap in caps.values():
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    collapsed_cap = cv2.VideoCapture(video_paths[outcome])
    
    # === Play through blended superposition ===
    last_blended = None
    for i in range(play_frames):
        frames = []
        for k, cap in caps.items():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
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
            # if i < int(fps):
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
    
    # === Lerp transition from superposition to collapsed frames (dynamic) ===transition_frames = 30
    for i in range(transition_frames):
        # Read next blended superposition frame
        frames = []
        for k, cap in caps.items():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()
            if ret:
                frame = frame.astype(np.float32)
                frames.append(frame)
        # Read next collapsed frame
        ret, collapsed_frame = collapsed_cap.read()
        if not ret:
            collapsed_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, collapsed_frame = collapsed_cap.read()
        if not ret or len(frames) != 4:
            break
        blended = sum(frames) / 4.0
        blended = np.clip(blended, 0, 255).astype(np.uint8)
        blended_f = blended.astype(np.float32)
        collapsed_f = collapsed_frame.astype(np.float32)
        alpha = (i + 1) / transition_frames
        frame = (1 - alpha) * blended_f + alpha * collapsed_f
        frame = np.clip(frame, 0, 255).astype(np.uint8)
        # Display measured outcome text during transition
        cv2.putText(
            frame, f'measured {outcome}', (30, 120),
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

    # Do not release collapsed_cap; continue to play through it at current location
    for i in range(play_frames):
        ret, frame = collapsed_cap.read()
        if not ret:
            collapsed_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = collapsed_cap.read()
        if not ret:
            break
        # Display 'collapsed' text for the first second
        if i < int(fps):
            cv2.putText(
                frame, 'collapsed', (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4, cv2.LINE_AA
            )
        cv2.imshow("Quantum Video", frame)
        key = cv2.waitKey(int(1000 / fps)) & 0xFF
        if key == 27:
            for cap in caps.values():
                cap.release()
            collapsed_cap.release()
            cv2.destroyAllWindows()
            exit()
    
    # === Lerp transition from collapsed back to superposition (dynamic) ===
    # Reset all video captures to the first frame for superposition
    # for cap in caps.values():
    #     cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    # collapsed_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    transition_frames = 30
    for i in range(transition_frames):
        # Read next collapsed frame
        ret, collapsed_frame = collapsed_cap.read()
        if not ret:
            collapsed_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, collapsed_frame = collapsed_cap.read()
        if not ret:
            break
        collapsed_f = collapsed_frame.astype(np.float32)

        # Read next blended superposition frame
        frames = []
        for k, cap in caps.items():
            ret2, frame = cap.read()
            if not ret2:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret2, frame = cap.read()
            if ret2:
                frame = frame.astype(np.float32)
                frames.append(frame)
        if len(frames) != 4:
            break
        blended = sum(frames) / 4.0
        blended = np.clip(blended, 0, 255).astype(np.uint8)
        blended_f = blended.astype(np.float32)

        # Lerp from collapsed to blended (reverse direction)
        alpha = (i + 1) / transition_frames
        frame = (1 - alpha) * collapsed_f + alpha * blended_f
        frame = np.clip(frame, 0, 255).astype(np.uint8)
        cv2.imshow("Quantum Video", frame)
        key = cv2.waitKey(int(1000 / fps)) & 0xFF
        if key == 27:
            for cap in caps.values():
                cap.release()
            collapsed_cap.release()
            cv2.destroyAllWindows()
            exit()
    collapsed_cap.release()
