# NavWareSet SFM Analysis

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://drive.google.com/file/d/14xYS15ttaP-WOrjsjgti_cuilx-lQHE3/view?usp=sharing)

## Overview
This repository contains data and analysis tools for studying **robot–human interactions** using the **NavWareSet dataset**.  
It focuses on calibrating and evaluating the **Social Force Model (SFM)** with selected robot–pedestrian interaction tracks.

## Contents
- **NavWareSet_SFM.ipynb**  
  Jupyter notebook implementing:
  - Data loading from selected track files  
  - Preprocessing and synchronization  
  - Simulation of pedestrian trajectories using the Social Force Model  
  - RMSE-based evaluation of model fit  
  - Visualization of real vs. simulated trajectories  

- **CSV track files (`s_track_sceneXX_colY_from_<timestamp>.csv`)**  
  Extracted subsets of the NavWareSet dataset. Each file corresponds to a specific scene and collection column.  
  - `sceneXX` → scenario ID (e.g., scene 21, 34, 47, 8)  
  - `colY` → collection column (e.g., different pedestrians or robot tracks)  
  - `from_<timestamp>` → dataset export time or unique identifier  

- **README.md**  
  Repository documentation.

## Getting Started
### Requirements
- Python 3.9+
- Jupyter Notebook or Google Colab
- Core libraries: `numpy`, `pandas`, `matplotlib`, `scipy`
- [UAIbotPy](https://github.com/UAIbot/UAIbotPy) (SFM simulation support)

### Usage
1. Open the notebook locally with Jupyter, or click the **Colab badge** above.  
2. Upload the CSV track files if running in Colab.  
3. Run the notebook cells step by step to reproduce the simulations and analysis.  

### Example Workflow
- Select a track file from `s_track_scene*.csv`  
- Run the SFM simulation with initial parameters  
- Optimize parameters with L-BFGS-B  
- Compare simulated trajectories with real pedestrian data  
- Save and visualize results as plots or animations  

## License
This repository is released under the MIT License. See [LICENSE](LICENSE) for details.

## Citation
If you use this code or data in your research, please cite the **NavWareSet dataset paper**:

> Brayan, J., Deng, S., Alves Neto, A., Okunevich, I., Krajnik, T., Bremond, F., & Yan, Z.  
> *NavWareSet: A Dataset of Socially Compliant and Non-Compliant Robot Navigation*.  
> The International Journal of Robotics Research, 2025.

