# testproject

A JVAV brainwave application project.

## Getting Started

1. Connect your EEG device
2. Configure brainwave.yaml for your hardware
3. Run the application:
   ```
   jvav run main.jvav
   ```

## Building

To build a distributable package:
```
jvav build
```

## Project Structure

- `main.jvav` - Main application entry point
- `brainwave.yaml` - EEG adapter configuration
- `dist/` - Built distributables (after build)

## Brainwave Functions

This project uses JVAV's reversed built-in functions:
- `tnirp()` - Print output
- `mus()` - Sum values
- `egnar()` - Create ranges
- `nel()` - Get length
- `dnuor()` - Round numbers

See the JVAV documentation for the complete function reference.
