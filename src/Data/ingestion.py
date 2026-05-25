from pathlib import Path
import hashlib

import requests


# link to page: https://zenodo.org/records/11295916
ZENODO_RECORD_ID = "11295916"
ZENODO_RECORD_URL = f"https://zenodo.org/api/records/{ZENODO_RECORD_ID}"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "datasets" / "raw"


def fetch_record_metadata(record_id: str) -> dict:
    """
    Fetch metadata for a published Zenodo record.

    This function does not download the dataset itself. It only queries the
    Zenodo REST API and returns the JSON metadata associated with a specific
    record ID. The metadata contains information such as title, DOI, version,
    publication date, available files, file sizes, checksums, and download URLs.

    Args:
        record_id: Zenodo record identifier.

    Returns:
        A dictionary containing the parsed JSON response from the Zenodo API.

    Raises:
        requests.HTTPError: If Zenodo returns an unsuccessful HTTP response.
        requests.Timeout: If the request takes longer than the configured timeout.
        requests.RequestException: For other network-related errors.
    """

    response = requests.get(f"https://zenodo.org/api/records/{record_id}", timeout=30)
    response.raise_for_status()
    return response.json()


def print_record_summary(record: dict) -> None:
    """
    Print a human-readable summary of a Zenodo record.

    This is useful as a first inspection step before downloading anything. It
    shows the dataset identity and the available raw files, including each
    file's size, checksum, and direct API download URL.

    Args:
        record: Metadata dictionary returned by fetch_record_metadata().

    Returns:
        None.
    """
    metadata = record["metadata"]

    print("=== RECORD ===")
    print(f"ID: {record['id']}")
    print(f"Title: {metadata.get('title')}")
    print(f"DOI: {metadata.get('doi')}")
    print(f"Publication date: {metadata.get('publication_date')}")
    print(f"Version: {metadata.get('version')}")

    print("\n=== FILES ===")
    for file in record.get("files", []):
        print(f"Name: {file['key']}")
        print(f"Size: {file['size']:,} bytes")
        print(f"Checksum: {file.get('checksum')}")
        print(f"Download URL: {file['links']['self']}")
        print()


def download_file(url: str, output_path: Path) -> None:
    """
    Download a file from a URL and save it locally.

    The file is streamed in chunks instead of being loaded fully into memory.
    This matters because datasets can be large. The parent directory is created
    automatically if it does not exist.

    Args:
        url: Direct download URL for the file.
        output_path: Local path where the downloaded file will be stored.

    Returns:
        None.

    Raises:
        requests.HTTPError: If the server returns an unsuccessful HTTP response.
        requests.Timeout: If the request takes longer than the configured timeout.
        requests.RequestException: For other network-related errors.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()

        with output_path.open("wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)


def calculate_md5(path: Path) -> str:
    """
    Calculate the MD5 checksum of a local file.

    Zenodo provides file checksums in its metadata. After downloading a file,
    this function lets us verify that the local file matches the checksum
    published by Zenodo.

    Args:
        path: Path to the local file.

    Returns:
        The hexadecimal MD5 checksum string.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    digest = hashlib.md5()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)

    return digest.hexdigest()

#------------------------------------------------------------------------------------------------------------------

def main() -> None:
    record = fetch_record_metadata(ZENODO_RECORD_ID)
    print_record_summary(record)

    file_metadata = record["files"][0]
    download_url = file_metadata["links"]["self"]
    output_path = RAW_DATA_DIR / file_metadata["key"]

    download_file(download_url, output_path)

    expected_checksum = file_metadata["checksum"].replace("md5:", "")
    actual_checksum = calculate_md5(output_path)

    if actual_checksum != expected_checksum:
        raise ValueError(
            f"Checksum mismatch. Expected {expected_checksum}, got {actual_checksum}"
        )

    print(f"Downloaded and validated: {output_path}")


if __name__ == "__main__":
    main()