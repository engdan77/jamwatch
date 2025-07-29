# JamWatch ⌚︎🎧

## Requirements

```shell
sudo apt-get install mtp-tools
```

## Usage
### Start as server waiting for button event (example)
```shell
sudo /home/user/.local/bin/uv run jamwatch start-server /home/user/mp3
```

## Notes for lgpio on Raspberry Pi
Requires for me install `lgpio` package run the following commands:
```shell
sudo apt-get install swig
sudo apt-get install liblgpio-dev
```

