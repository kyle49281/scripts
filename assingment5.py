import gzip
import numpy as np

def extract_hr_numbers_gz(file_path):
    vm = []
    hr = []
    ci_list = []
    trig_para = []
    spectral = []
    
    with gzip.open(file_path, 'rt') as file:  # 'rt' opens it in text mode
        for line in file:
            vm.append(line[102:107].strip())  # Visual magnitude
            hr.append(line[0:4].strip())      # Harvard Revised Number
            ci_list.append(line[109:114].strip())  # Color Index
            trig_para.append(line[161:166].strip())  # Parallax
            spectral.append(line[127:147].strip())  # Spectral type

    # Convert 'vm' and 'trig_para' to floats, replacing invalid entries with None
    vm = [float(x) if x else None for x in vm]
    trig_para = [float(x) if x and float(x) > 0.01 else None for x in trig_para]

    # Step 1: Calculate distances from parallax (in parsecs)
    distances = [
        1 / p if p is not None and p > 0 else None for p in trig_para
    ]

    # Step 2: Calculate absolute magnitude using the distance and apparent magnitude
    abs_Vmag = [
        vm[i] - 5 * (np.log10(distances[i]) - 1) if vm[i] is not None and distances[i] is not None else None
        for i in range(len(vm))
    ]

    # Create a list of only the floats, but maintain their original indices
    filtered_data = [(i, float(x)) for i, x in enumerate(abs_Vmag) if x is not None]

    # Find the tuple with the minimum absolute magnitude (the brightest star)

    min_index, min_value = min(filtered_data, key=lambda x: x[1])

    # Calculate distance using the parallax of the brightest star
    distance = distances[min_index]

    # Output the details of the brightest star
    print(f'''The Harvard Revised Number of the brightest absolute magnitude star is {hr[min_index]}.
Its visual magnitude is {vm[min_index]}.
Its colour index is {ci_list[min_index]}.
Its trigonometric parallax is {trig_para[min_index]} arcsec.
Its distance is {distance:.2f} parsecs.
Its absolute magnitude is {min_value:.2f}.
Its spectral type is {spectral[min_index]}.''')



# Path to your gzipped star catalog file
file_path = 'catalog2.gz'  # Replace with the actual file path

# Call the function to extract and display HR numbers
extract_hr_numbers_gz(file_path)