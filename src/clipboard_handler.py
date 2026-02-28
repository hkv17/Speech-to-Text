import subprocess
import pyperclip


def copy_to_clipboard(text: str) -> None:
    try:
        pyperclip.copy(text)
    except Exception:
        # Fallback to pbcopy if pyperclip fails
        subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
