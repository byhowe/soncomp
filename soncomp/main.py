from dataclasses import dataclass
import os
import os.path
import subprocess


@dataclass
class transcoder:
    _target_format: str
    _bitrate: int

    @classmethod
    def mp3(cls) -> "transcoder":
        return cls("mp3", 192)

    @classmethod
    def opus(cls) -> "transcoder":
        return cls("opus", 128)

    @classmethod
    def aac(cls) -> "transcoder":
        return cls("aac", 256)

    @property
    def bitrate(self) -> int:
        return self._bitrate

    @bitrate.setter
    def bitrate(self, br: int):
        self._bitrate = br

    def command(self, input: str, output: str) -> list[str]:
        match self._target_format:
            case "mp3":
                return [
                    "ffmpeg",
                    "-i",
                    input,
                    "-map",
                    "0:0",
                    "-b:a",
                    f"{self.bitrate}k",
                    "-v",
                    "0",
                    "-f",
                    "mp3",
                    output,
                ]
            case "opus":
                return [
                    "ffmpeg",
                    "-i",
                    input,
                    "-map",
                    "0:0",
                    "-b:a",
                    f"{self.bitrate}k",
                    "-v",
                    "0",
                    "-c:a",
                    "libopus",
                    "-f",
                    "opus",
                    output,
                ]
            case "aac":
                return [
                    "ffmpeg",
                    "-i",
                    input,
                    "-map",
                    "0:0",
                    "-b:a",
                    f"{self.bitrate}k",
                    "-v",
                    "0",
                    "-c:a",
                    "aac",
                    "-f",
                    "adts",
                    output,
                ]
        raise


def main():
    tc = transcoder.opus()
    for root, _, files in os.walk("."):
        flacs = (f for f in files if f.lower().endswith(".flac"))
        flacs = (os.path.join(root, f) for f in flacs)
        flacs = list(flacs)
        for i, flac in enumerate(flacs, start=1):
            print(f"[{i}/{len(flacs)}] {flac.split('/')[-1]}")
            out = flac.replace(".flac", ".ogg")
            subprocess.run(tc.command(flac, out))
            os.remove(flac)


if __name__ == "__main__":
    main()
