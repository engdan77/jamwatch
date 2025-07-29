# JamWatch ⌚︎🎧

## Background

...

## Requirements

```shell
# mtp-tool - https://launchpad.net/ubuntu/jammy/+package/mtp-tools
sudo apt-get install mtp-tools
```

## Usage
### Start as server waiting for button event (example)

Ensure you have [UV](https://docs.astral.sh/uv/) installed available to root user - installation instructions [here](https://docs.astral.sh/uv/getting-started/installation/).

```shell
sudo uv run jamwatch start-server /home/user/mp3
```

## Software design

### Class diagram

```mermaid
classDiagram
    class AppError {
        <<Exception>>
    }
    class MountError {
        <<Exception>>
    }
    class FileWriteError {
        <<Exception>>
    }
    
    class Mount {
        <<Protocol>>
        +str path
        +is_mounted() bool
        +mount() bool
        +free_space() int
    }
    
    class LocalMount {
        +is_mounted() bool
        +mount()
        +free_space() int
    }
    
    class MtpMount {
        -_detect_command() tuple
        +is_mounted(detect_string: str) bool
        +free_space() int
    }
    
    class MountChecker {
        -Mount mount
        -Blink blinker
        -int sleep_secs
        -bool running
        +start()
        -_start_loop()
        +stop()
    }
    
    class FileWriter {
        <<Protocol>>
        +str path
        +write_content(content: bytes, filename: str)
        +erase()
    }
    
    class LocalFileWriter {
        +str path
        +write_content(content: bytes, filename: str)
        +erase()
    }
    
    class MtpFileWriter {
        +write_content(content: bytes, filename: str)
        +erase()
        -_get_all_files() list
    }
    
    class Orchestrator {
        -OrchestratorParams orchestrator_config
        -Config config
        -bool running
        -bool copy_in_progress
        +start_loop()
        +stop()
        +loop()
        +copy()
    }
    
    class OrchestratorParams {
        +FileReader file_reader
        +FileWriter file_writer
        +Mount mount
        +Blink progress_blinker
        +Blink mount_blinker
    }

    AppError <|-- MountError
    AppError <|-- FileWriteError
    
    Mount <|.. LocalMount
    Mount <|.. MtpMount
    
    FileWriter <|.. LocalFileWriter
    FileWriter <|.. MtpFileWriter
    
    MountChecker --> Mount
    Orchestrator --> OrchestratorParams
    OrchestratorParams --> Mount
    OrchestratorParams --> FileWriter
```


## Notes for lgpio on Raspberry Pi
Requires for me install `lgpio` package run the following commands:
```shell
sudo apt-get install swig
sudo apt-get install liblgpio-dev
```

