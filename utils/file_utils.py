import io

def download_filename(basics: dict, ext: str) -> str:
    name = basics.get("name", "resume").replace(" ", "_")
    return f"{name}_resume.{ext}"
