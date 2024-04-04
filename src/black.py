import argparse
from .util import push


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a Pixlet script and push the WebP output to a Tidbyt")
    parser.add_argument("device_id", help="Tidbyt device ID")
    args = parser.parse_args()
    with open("dist/black.webp", "rb") as image_file:
        image_bytes = image_file.read()
        for i in range(4):
            installation_id = f"black{i:02d}"
            push(image_bytes, args.device_id, installation_id, True)

