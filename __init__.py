import math
import torch


class AudioDuration:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "extra_seconds": ("INT", {"default": 0, "min": 0, "max": 9999}),
            },
            "optional": {
                "min_duration": ("INT", {
                    "default": 4,
                    "min": 0,
                    "max": 9999,
                    "tooltip": (
                        "Si la duracion calculada (ceil + extra_seconds) es mayor "
                        "que 0 pero menor que min_duration, se eleva a min_duration. "
                        "Util cuando el ultimo chunk de audio queda por debajo del "
                        "minimo aceptado por el generador de video (ej. Seedance "
                        "exige >= 4s) y no quieres que el gate descarte ese chunk. "
                        "Cuando la duracion es 0 (audio vacio) NO se eleva, asi los "
                        "crops fuera del audio siguen siendo bloqueados por el gate. "
                        "Default 4 (minimo de Seedance). Pon 0 para desactivar."
                    ),
                }),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("duration",)
    FUNCTION = "calculate"
    CATEGORY = "audio"

    def calculate(self, audio, extra_seconds, min_duration=4):
        waveform = audio["waveform"]      # shape: (1, 1, samples)
        sample_rate = audio["sample_rate"]
        num_samples = waveform.shape[-1]
        duration_seconds = num_samples / sample_rate
        duration = math.ceil(duration_seconds) + extra_seconds
        if 0 < duration < min_duration:
            duration = min_duration
        return (duration,)


NODE_CLASS_MAPPINGS = {
    "AudioDuration": AudioDuration,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AudioDuration": "Audio Duration (INT)",
}
