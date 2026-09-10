# Glowing Heart Particles Animation

An animated visualization of a heart shape made of glowing text particles, featuring the word "Melody" and a centered "I LOVE YOU" message.

## Features

✨ **Particle Animation**
- Heart shape generated using parametric equations
- 120+ animated particles with varying sizes and positions
- Each particle displays "Melody" in shades of blue and cyan

🌟 **Visual Effects**
- Soft glow effect using multi-layer alpha blending
- Sine wave-based particle flickering with random noise
- Gradual fade-in animation as particles appear
- Subtle position jitter for organic motion
- Rotating text for visual interest

❤️ **Center Display**
- Bold "I LOVE YOU" text at the heart's center
- Pulsating glow effect
- Soft blue/cyan color scheme

## Requirements

- Python 3.7+
- Pygame

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/omogbaiprecious-456/glowing-heart-particles.git
   cd glowing-heart-particles
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the animation:
```bash
python main.py
```

### Controls

- **Close Window** - Exit the application
- **Press Q** - Quit the application

## Technical Details

### Parametric Heart Equation

The heart shape is generated using the classic parametric equations:

```
x(t) = 16 * sin³(t)
y(t) = 13 * cos(t) - 5 * cos(2t) - 2 * cos(3t) - cos(4t)
```

Particles are positioned along this curve and rendered with varying properties to create the animation.

### Animation Pipeline

1. **Update Phase**: Particles update their alpha, flicker state, and jitter
2. **Glow Layers**: Multiple passes render progressively larger text with decreasing alpha
3. **Main Particles**: Bright text rendering for main visibility
4. **Center Text**: "I LOVE YOU" message with its own glow effect
5. **Display**: Frame is rendered at 45 FPS

### Performance

- **Window**: 800x600 pixels
- **FPS**: 45 frames per second
- **Particles**: 120 text particles
- **Background**: Pure black for contrast

## Customization

You can customize the animation by modifying the constants in `main.py`:

- `WINDOW_WIDTH`, `WINDOW_HEIGHT` - Display size
- `FPS` - Animation frame rate
- `PARTICLE_COUNT` - Number of particles
- `BLUE_PALETTE` - Particle colors
- `scale` parameter in `generate_heart_particles()` - Heart size

## Code Structure

- **Particle Class**: Manages individual particle state and animation
- **generate_heart_particles()**: Creates particles along the heart curve
- **render_glow_text()**: Helper for glow effect rendering
- **main()**: Main animation loop and Pygame initialization

## License

Free to use and modify for personal projects.
