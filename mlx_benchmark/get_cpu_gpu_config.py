import subprocess
import re
import mlx.core as mx


def get_system_info():
    hardware_result = subprocess.run(
        ["system_profiler", "SPHardwareDataType"], capture_output=True, text=True
    )
    hardware_data = hardware_result.stdout

    display_result = subprocess.run(
        ["system_profiler", "SPDisplaysDataType"], capture_output=True, text=True
    )
    display_data = display_result.stdout

    chipset_pattern = r"Chip: (.+)"
    chipset_match = re.search(chipset_pattern, hardware_data)
    chipset_model = (
        chipset_match.group(1).strip() if chipset_match else "Unknown Chipset"
    )

    cores_pattern = (
        r"Total Number of Cores: (\d+) \((\d+) performance and (\d+) efficiency\)"
    )
    super_cores_pattern = (
        r"Total Number of Cores: (\d+) \((\d+) Super and (\d+) Performance\)"
    )
    match = re.search(cores_pattern, hardware_data)
    super_match = re.search(super_cores_pattern, hardware_data)
    if super_match:
        total_cores, super_cores, performance_cores = super_match.groups()
        efficiency_cores = None
    elif match:
        total_cores, performance_cores, efficiency_cores = match.groups()
        super_cores = None
    else:
        total_cores = performance_cores = efficiency_cores = super_cores = None

    gpu_cores_pattern = r"Total Number of Cores: (\d+)"
    gpu_match = re.search(gpu_cores_pattern, display_data)
    gpu_cores = gpu_match.group(1) if gpu_match else "Unknown"

    ram_pattern = r"Memory: (.+)"
    ram_match = re.search(ram_pattern, hardware_data)
    ram = ram_match.group(1).strip() if ram_match else "Unknown RAM"
    ram = ram.split(" ")[0]

    chipset_model = chipset_model.split("Apple")[-1]
    if super_cores:
        formatted_output = f"{chipset_model} ({super_cores}S+{performance_cores}P+{gpu_cores}GPU+{ram}GB)"
    else:
        formatted_output = f"{chipset_model} ({efficiency_cores}E+{performance_cores}P+{gpu_cores}GPU+{ram}GB)"
    return formatted_output


description = f"{get_system_info()} - mlx: {mx.__version__}"
print(description)
