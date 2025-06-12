# 🌿 LI-COR LI-6800 Background Programs for leaf-level gas exchange measurement for photosynthesis model calibration

These LI-6800 Background Program scripts automate **Dynamic Assimilation Technique (DAT)** measurements across a series of **light flux levels** and **temperatures**, while ramping CO₂ and tagging each curve with a unique identifier (`CurveID`). It’s designed for efficient, high-resolution A–Ci curves to calibrate photosynthesis models.

---

## Key Features

- 🚀 **DAT-Style A–Ci Curves**: Continuous CO₂ ramping at varied lights and temperatures.
- 🤖 **Fully Scripted Workflow**: Minimal user input needed. Just start the script, and it handles light, temperature, and CO₂ changes dynamically.
- 📈 **Model-Ready Output**: Facilitates **robust calibration** of biochemical models of photosynthesis, including temperature and light dependencies.

___

## How to Use

### 1. 📥 Transfer the Scripts to the LI-COR

1. Download the `.py` script files (e.g., `ACi_Light_Sweep.py`) to your computer, and then to a USB thumbdrive.
2. Connect the head to the console and turn the LI-6800 on. Connect the USB thumbdrive to the LI-6800.
3. Use the LI-6800 file browser under `Tools`->`Manage Files:`. Select `Copy files to LI-6800`, and under the `Copy to` drop-down, select `BP Directory`. Find the protocol .py files, select them and press `Copy` to transfer the file to the device. Safely eject the USB with `Eject`.
4. Add user variables under the `Constants` -> `User` tab. Press `Add` followed by `Edit` and rename the variable `CurveID`. Make another variable and rename it `Reponse`.

---


### 2. ⚙️ Run the Program and Set User Inputs

On the LI-COR LI-6800 console interface, navigate to the `Programs` tab, then to `BP Builder` and locate the programs downloaded in Step 1. Select the desired program and press `Run`. 

> 📝 A dialog will appear to allow the editing of the following **User inputs**:

| **Variable**     | **Label in UI**      | **Description**                                | **Units**                         | **Example Default**            |
|------------------|----------------------|------------------------------------------------|-----------------------------------|-------------------------------|
| `begin_co2`      | Starting CO₂         | Starting reference CO₂ for ramp                | µmol mol⁻¹                        | `10`                          |
| `init_wait`      | Pre ramp wait        | Equilibration time before starting ramp        | min                               | `1`                           |
| `end_co2`        | Ending CO₂           | Ending reference CO₂ for ramp                  | µmol mol⁻¹                        | `2000`                        |
| `post_co2`       | Post-ramp CO₂        | CO₂ setpoint after ramp                        | µmol m⁻² s⁻¹                      | `400`                         |
| `ramp_rate`      | Ramp rate            | Rate of CO₂ change during ramp                 | µmol mol⁻¹ min⁻¹                  | `300`                         |
| `light_levels`   | Light levels         | List of light intensities used per ramp        | µmol m⁻² s⁻¹                      | `[0,200,600,1200,1600,2000]`  |
| `temperatures`   | Temperatures         | List of air temperatures per light level       | °C                                | `[25,30,35,38,40,43]`         |
| `log_int`        | Logging interval     | Logging interval during CO₂ ramp               | s                                 | `5`                           |
| `post_wait`      | Post ramp wait       | Time to wait after ramp ends                   | min                               | `0`                           |
| `pwlog`          | Log post ramp        | Logging interval after ramp (if checked)       | s (checkable)                     | `Unchecked`, value: `15`      |

You only need to set these once. The script reads them at runtime.

---
