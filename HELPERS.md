# Instructions for helpers

In order to maximise the time availble for the coding task please do the following in advance of the session
1. Fork this repo
1. Start a codespace on your fork (you will be prompted to authorise read access to `opensafely/server-instructions`, please do so)
1. Pull the required opensafely images:
```sh
opensafely pull ehrql:v1
opensafely pull python:v2
opensafely pull r:latest
```
4. Make sure RStudio opens correctly, and
    - The file browser has the workspace directory open. If it does not, point it at `/workspaces/{name-of-your-repo}
    - The git integration has activated (there is a grey/red/green sideways Git button in the toolbar)