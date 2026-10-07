# Ceiling Vibration Trigger Recorder

A recovered 2020 physical-computing project built to document unexplained loud impacts coming from inside an apartment ceiling when building management wanted evidence.

The system combined an **Arduino + piezo vibration sensor** with a **Raspberry Pi + USB PlayStation camera**. The Arduino sampled vibrations in the ceiling and streamed readings over USB serial. The Raspberry Pi learned a short baseline from the sensor, then triggered a timestamped audio/video recording when a later vibration exceeded that baseline.

## How it worked

1. A piezo sensor connected to Arduino analog input `A0` sampled vibrations.
2. The Arduino took repeated analog readings, retained the local peak, smoothed the decay, and sent significant readings over serial at 9600 baud.
3. The Raspberry Pi listened on `/dev/ttyACM0` and used the first batch of numeric readings as a baseline.
4. A reading above that baseline triggered `ffmpeg`.
5. `ffmpeg` captured audio from ALSA and video from `/dev/video0`, producing a timestamped AVI clip.

The surviving final prototype used a 100-reading calibration window and recorded roughly three-second 640×480 clips at 25 fps.

## Repository structure

- `recorder.py` — cleaned, configurable version of the final Raspberry Pi trigger/recording loop.
- `arduino/piezo_trigger.ino` — recovered Arduino piezo-sensor sketch.
- `archive/prototypes/` — selected original Python iterations showing the path from simple serial-trigger capture to the calibrated final version.

## Requirements

### Raspberry Pi / Linux

- Python 3
- `ffmpeg`
- an ALSA-compatible audio input
- a V4L2 camera such as `/dev/video0`
- Arduino connected over USB serial

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Example:

```bash
python recorder.py --serial-port /dev/ttyACM0 --camera /dev/video0
```

## Archive notes

The original folder also contained generated AVI/WAV recordings, Python cache files, throwaway serial tests, and incomplete Arduino sketches. Those are intentionally not included here. The surviving AVI/WAV files were test recordings made by manually knocking / triggering the sensor during development, not the actual ceiling-noise evidence. The real evidence recordings may still exist on an older Raspberry Pi or SD card, but they were not present in this recovered archive.

This is archival code from 2020. The cleaned entry point keeps the original architecture and trigger behavior while replacing hard-coded filesystem paths and shell-string construction with configurable arguments and direct subprocess invocation.