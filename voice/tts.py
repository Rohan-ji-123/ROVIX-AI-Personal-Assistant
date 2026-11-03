import subprocess

def speak(text):
    """Speak text using Windows built-in speech synthesis."""

    if not isinstance(text,str) or not text.strip():
        return

    #Escape single quote for powershell
    safe_text = text.replace("'", "''")

    powershell_command = (
        "Add-Type -AssemblyName System.Speech; "
        "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$speaker.Speak('{safe_text}');"
        "$speaker.Dispose()"
    )     
    try: 
        subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                powershell_command
            ],
            check=True,
            timeout=60,
            capture_output=True,
            text=True,
        )
    except(subprocess.SubprocessError,OSError) as error:
        print(f"ROVIX: Voice output failed: {error}")

if __name__ == "__main__":
    speak("Hello! I am ROVIX , How can i help you?")           