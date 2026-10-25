import os


def handle_command():
    """Daftar perintah berdasarkan file di folder modules."""
    folder = os.path.dirname(os.path.abspath(__file__))
    names = sorted(
        f[:-3] for f in os.listdir(folder)
        if f.endswith(".py") and f != "__init__.py"
    )
    if names:
        return "Perintah: " + ", ".join(names)
    return "No commands available."