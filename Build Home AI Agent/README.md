# Build Home AI Agent

English | [中文](README_zh.md)

## Introduction



## Documentation



## Related Resources

[Download Here](https://pan.baidu.com/s/5P4zJnQ1tJkycI24FEcJC4Q)

## Code

### WSL Related Commands

Manual installation from Microsoft official website: https://learn.microsoft.com/en-us/windows/wsl/install-manual

```shell
# Check current WSL version
wsl -v

# Install WSL framework (if wsl -v does not show a version)
wsl --install

# Switch default WSL version to WSL2
wsl --set-default-version 2

# List installed WSL distributions and their status
wsl --list --verbose

# Completely remove a distribution
wsl --unregister Ubuntu-22.04

# Install a specific distribution
wsl --install Ubuntu-22.04

# Enter a specific distribution
wsl -d Ubuntu-22.04

# Import an external distribution from a file
# (modify the install path and tar file path as needed)
wsl --import Ubuntu-jjdyycm C:\Users\astercasc X:\red.panda\new\jjdyycm.tar

```

### Linux Related (Native Linux or after entering a container using WSL -d <distro>)



### Windows Commands




## Tech Stack

- [WSL](https://learn.microsoft.com/en-us/windows/wsl/)