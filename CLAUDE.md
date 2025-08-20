# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Numun is a Conway's Game of Life implementation with a GUI built using Kivy/KivyMD and a separate simulator engine. The project is structured as a modular Python application with a graphical interface for visualizing and interacting with cellular automata.

## Architecture

### Core Components

- **GUI Layer** (`gui/`): KivyMD-based graphical interface
  - `main.py`: Entry point, handles window management and multi-monitor setup
  - `components/grid/`: Interactive cellular grid visualization with zooming and cell manipulation
  - `components/cell/`: Individual cell rendering and state management
  - `pages/interface/`: Main application interface screen
  
- **Simulator Engine** (`simulator/`): Conway's Game of Life logic
  - `main.py`: Core `Simulator` class implementing Game of Life rules using NumPy/SciPy convolution
  - Uses a "water pool" technique with 256x256 buffer for edge handling during evolution

### Key Architectural Patterns

1. **Separation of Concerns**: GUI and simulation logic are completely separated
2. **Component-Based UI**: Kivy components with `.kv` files for UI layout
3. **Batch Cell Updates**: Grid updates cells in batches (100 at a time) to prevent UI freezing
4. **Efficient Simulation**: Uses convolution for neighbor counting rather than nested loops

## Development Commands

### Running the Application
```bash
# Install dependencies first
pip install -r requirements.txt

# Run the GUI application
cd gui
python main.py
```

### Key Controls (when running)
- **Ctrl+Z**: Toggle zoom mode on/off
- **Ctrl+6**: Zoom out (decrease cell size)
- **Ctrl+=**: Zoom in (increase cell size)
- **Spacebar**: Advance simulation by one tick
- **Mouse scroll** (when zoom enabled): Zoom in/out

## Critical Implementation Details

### Grid-Simulator Integration
The GUI Grid component (`gui/components/grid/grid.py`) contains a duplicate `Simulator` class that should be kept in sync with `simulator/main.py`. When the user presses spacebar:
1. Grid extracts cell states into a 2D list
2. Creates/updates Simulator instance
3. Calls `simulator.tick()`
4. Updates GUI cells based on new simulator state

### Cell Size and Window Management
- Application enforces square window dimensions
- Grid calculates minimum/maximum cell sizes based on window dimensions and grid size
- Supports multi-monitor setups with automatic monitor detection

### Performance Considerations
- Large grids use batched cell creation to prevent UI blocking
- Grid dimension changes trigger cell addition/removal in batches
- Zoom operations directly manipulate cell sizes rather than recreating the grid

## Dependencies
- **kivy==2.3.1**: Core GUI framework
- **kivymd==1.2.0**: Material Design widgets
- **numpy==2.2.5**: Efficient array operations for simulation
- **scipy==1.15.2**: Convolution operations for neighbor counting
- **screeninfo==0.8.1**: Multi-monitor support
- **msgpack==1.1.0**: Serialization (likely for save/load functionality)

## Current Limitations
- Save/load/export functionality is stubbed out in the Simulator class
- Grid dimension changes are partially implemented
- Cell removal functionality is not implemented