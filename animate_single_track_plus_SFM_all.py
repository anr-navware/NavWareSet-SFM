import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import uaibot as ub
import glob

def get_frame_rate(df):
    if len(df) < 2:
        return None
    time_diffs = df['timestamp'].diff().dropna()
    median_diff_ns = time_diffs.median()
    fps = 1e9 / median_diff_ns
    return fps

def get_average_speed(df):
    if len(df) < 2:
        return 0.0
    dx = df['x'].diff()
    dy = df['y'].diff()
    distances = np.sqrt(dx**2 + dy**2)
    total_distance = distances.sum()
    total_time_ns = df['timestamp'].iloc[-1] - df['timestamp'].iloc[0]
    total_time_s = total_time_ns / 1e9
    if total_time_s == 0:
        return 0.0
    avg_speed = total_distance / total_time_s
    return avg_speed

# Find all CSV files in the current directory that match the track pattern
csv_files = sorted(glob.glob("track_scene*.csv"))

for csv_file in csv_files:
    print(f"\nAnimating: {csv_file}")
    df = pd.read_csv(csv_file)
    df['timestamp'] = df['timestamp'].astype(float)
    df = df.sort_values('timestamp')

    frame_rate = get_frame_rate(df)
    print(f"Estimated frame rate: {frame_rate:.2f} FPS")

    initial_x = df['x'].iloc[0]
    initial_y = df['y'].iloc[0]
    final_x = df['x'].iloc[-1]
    final_y = df['y'].iloc[-1]
    robot_x = df['robot_x'].iloc[0]
    robot_y = df['robot_y'].iloc[0]

    ro = np.array([robot_x, robot_y])
    ra = np.array([initial_x, initial_y])
    g = np.array([final_x, final_y])
    ro_radius = 0.3  # Robot radius
    va0 = get_average_speed(df)

    # Create a Pedestrian object
    p = ub.Pedestrian(ra, g, va0=va0)

    # Create robot as an obstacle
    obstacle = ub.ObstacleColumn(ro, radius=ro_radius, name="robot", color="red", height=1)

    # Initialize simulation parameters
    dt = 0.1
    t_max = 10
    tolerance = 0.3

    # Lists to store simulation data
    positions = []
    robot = []
    time_steps = []

    t = 0
    k = 1
    while np.linalg.norm(p.ra - p.g) > tolerance and t < t_max:
        fag_result = p.fag()
        fdaq_result = p.fdaq(obstacle) * p.w(obstacle)
        p.va = p.va + (fag_result + fdaq_result) * dt
        p.ra = p.ra + p.va * dt
        try:
            new_robot_x = df['robot_x'].iloc[k]
            new_robot_y = df['robot_y'].iloc[k]
            new_ro = np.array([new_robot_x, new_robot_y])
            obstacle.ro = new_ro
        except:
            break
        positions.append(p.ra.flatten())
        robot.append(obstacle.ro.flatten())
        t += dt
        k += 1
        time_steps.append(t)

    positions = np.array(positions)
    robot = np.array(robot)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(df['x'], df['y'], 'k:', alpha=0.5, label='Person CSV Track')
    ax.plot(df['robot_x'], df['robot_y'], 'gray', linestyle=':', marker='x', alpha=0.5, label='Robot CSV Track')

    ax.set_xlim(min(positions[:, 0].min(), robot[:, 0].min(), df['x'].min(), df['robot_x'].min()) - 1,
                max(positions[:, 0].max(), robot[:, 0].max(), df['x'].max(), df['robot_x'].max()) + 1)
    ax.set_ylim(min(positions[:, 1].min(), robot[:, 1].min(), df['y'].min(), df['robot_y'].min()) - 1,
                max(positions[:, 1].max(), robot[:, 1].max(), df['y'].max(), df['robot_y'].max()) + 1)

    person_line, = ax.plot([], [], 'b.-', label='Person Trajectory')
    robot_line, = ax.plot([], [], 'orange', linestyle='--', marker='o', label='Robot Position')
    ax.scatter([ra[0]], [ra[1]], color='green', label='Start', zorder=5)
    ax.scatter([g[0]], [g[1]], color='red', label='Goal', zorder=5)
    ax.scatter([ro[0]], [ro[1]], color='orange', label='Robot Start', zorder=5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(f'Person and Robot Trajectories with Obstacle\n{csv_file}')
    ax.legend()
    ax.grid()
    ax.axis('equal')

    def init():
        person_line.set_data([], [])
        robot_line.set_data([], [])
        return person_line, robot_line

    def animate(i):
        person_line.set_data(positions[:i+1, 0], positions[:i+1, 1])
        robot_line.set_data(robot[:i+1, 0], robot[:i+1, 1])
        return person_line, robot_line

    ani = animation.FuncAnimation(
        fig, animate, frames=len(positions), init_func=init, blit=True, interval=100, repeat=False
    )

    plt.show()