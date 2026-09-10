from struct import unpack


def read_snr_measurement():
    """
    Reads a float measurement from a binary file and closes the file explicitly.


    Returns:
    - float: The unpacked measurement from the file.
    """
    try:
        f = open("/root/SNR", "rb")
        # Read 4 bytes and unpack into a float
        measurement_from_file = unpack("<f", f.read(4))
        measurement = measurement_from_file[0]
        f.close()  # Explicitly close the file
        return measurement
    except Exception as e:
        raise RuntimeError(f"Error reading measurement from {file_path}: {e}")
