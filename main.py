"""
Animated Glowing Heart Particle Animation
==========================================

This script creates an animated heart shape made of text particles using Pygame.
Each particle displays the word "Melody" in varying sizes and shades of blue/cyan,
with a flickering glow effect. A centered "I LOVE YOU" message floats at the heart's center.

Features:
- Parametric heart equation for particle positioning
- Soft glow effects with alpha blending
- Sine wave-based particle flickering with random noise
- Gradual fade-in animation over time
- Windowed display (800x600) at 30-60 FPS

Requirements:
- pygame

Usage:
    python main.py

Controls:
    - Close window or press Q to exit
"""

import pygame
import math
import random
from typing import List, Tuple

# ============================================================================
# CONFIGURATION
# ============================================================================

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 45
BACKGROUND_COLOR = (0, 0, 0)  # Black
PARTICLE_COUNT = 120

# Color palette: shades of blue and cyan
BLUE_PALETTE = [
    (100, 150, 255),  # Light blue
    (80, 180, 255),   # Sky blue
    (50, 200, 255),   # Cyan-blue
    (0, 220, 255),    # Cyan
    (100, 200, 255),  # Light cyan-blue
]

# ============================================================================
# PARTICLE CLASS
# ============================================================================

class Particle:
    """
    Represents a single text particle in the heart animation.
    
    Attributes:
        x, y: Position in screen space
        base_x, base_y: Position on the parametric heart curve
        alpha: Current opacity (0-255)
        max_alpha: Target maximum opacity
        size: Font size for rendering "Melody"
        color: RGB color tuple
        delay: Number of frames before this particle starts fading in
        flicker_phase: Current phase of flickering sine wave
        flicker_speed: How fast the particle flickers
        rotation: Text rotation in degrees
        created_at: Frame number when particle was created
    """
    
    def __init__(self, x: float, y: float, delay: int, size: int = 16):
        self.base_x = x
        self.base_y = y
        self.x = x
        self.y = y
        self.alpha = 0
        self.max_alpha = 200
        self.size = size
        self.color = random.choice(BLUE_PALETTE)
        self.delay = delay
        self.flicker_phase = random.uniform(0, 2 * math.pi)
        self.flicker_speed = random.uniform(0.08, 0.15)
        self.rotation = random.uniform(-15, 15)
        self.created_at = 0
        
        # Slight randomization for position jitter
        self.jitter_x = random.uniform(-2, 2)
        self.jitter_y = random.uniform(-2, 2)
    
    def update(self, frame: int):
        """
        Update particle state: fade-in, flicker, and jitter.
        
        Args:
            frame: Current frame number
        """
        # Fade in over delay frames
        if frame >= self.delay:
            progress = min(1.0, (frame - self.delay) / max(1, self.delay))
            self.alpha = int(self.max_alpha * progress)
        else:
            self.alpha = 0
        
        # Apply flickering: sine wave + random noise
        flicker_amount = math.sin(self.flicker_phase) * 0.6 + random.uniform(-0.2, 0.2)
        self.alpha = max(0, int(self.alpha * (0.7 + flicker_amount * 0.3)))
        
        # Update flicker phase for next frame
        self.flicker_phase += self.flicker_speed
        
        # Apply slight random jitter to position
        self.x = self.base_x + self.jitter_x + random.uniform(-1, 1)
        self.y = self.base_y + self.jitter_y + random.uniform(-1, 1)


# ============================================================================
# HEART SHAPE GENERATOR
# ============================================================================

def generate_heart_particles(center_x: int, center_y: int, scale: float = 150, 
                             particle_count: int = 120) -> List[Particle]:
    """
    Generate particles arranged in a heart shape using the parametric heart equation.
    
    The parametric heart equation:
        x(t) = 16 * sin³(t)
        y(t) = 13 * cos(t) - 5 * cos(2t) - 2 * cos(3t) - cos(4t)
    
    Args:
        center_x: X coordinate of heart center
        center_y: Y coordinate of heart center
        scale: Scaling factor for heart size
        particle_count: Number of particles to generate
    
    Returns:
        List of Particle objects arranged in heart shape
    """
    particles = []
    
    for i in range(particle_count):
        # Parameter t ranges from 0 to 2π
        t = (i / particle_count) * 2 * math.pi
        
        # Parametric heart equations
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        
        # Scale and center on screen
        x = center_x + x * scale / 30
        y = center_y - y * scale / 30  # Negate Y because screen coordinates are top-down
        
        # Vary particle size based on position (creates depth effect)
        size = random.randint(12, 24)
        
        # Stagger delay so particles fade in sequentially
        delay = int((i / particle_count) * 60)
        
        particle = Particle(x, y, delay, size)
        particles.append(particle)
    
    return particles


# ============================================================================
# GLOW RENDERING HELPER
# ============================================================================

def render_glow_text(font: pygame.font.Font, text: str, color: Tuple[int, int, int],
                     x: int, y: int, alpha: int, glow_passes: int = 3) -> pygame.Surface:
    """
    Render text with a soft glow effect using multiple alpha-blended passes.
    
    Args:
        font: Pygame font object
        text: Text to render
        color: RGB color
        x, y: Position to render at
        alpha: Opacity of main text (0-255)
        glow_passes: Number of glow layers (higher = softer glow)
    
    Returns:
        Surface with rendered glowing text
    """
    # Create a surface for the text with alpha channel
    text_surface = font.render(text, True, color)
    text_surface.set_alpha(alpha)
    
    return text_surface


# ============================================================================
# MAIN ANIMATION LOOP
# ============================================================================

def main():
    """Main animation loop."""
    
    # Initialize Pygame
    pygame.init()
    display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Glowing Heart Particles - I LOVE YOU")
    clock = pygame.time.Clock()
    
    # Create font objects
    particle_font = pygame.font.Font(None, 16)  # Will be scaled per particle
    center_font = pygame.font.Font(None, 80)
    center_font.bold = True
    
    # Generate heart particles
    center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
    particles = generate_heart_particles(center_x, center_y, scale=140, 
                                        particle_count=PARTICLE_COUNT)
    
    # Main animation state
    frame = 0
    running = True
    
    # ========================================================================
    # MAIN LOOP
    # ========================================================================
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
        
        # Update particles
        for particle in particles:
            particle.update(frame)
        
        # Clear screen with black background
        display.fill(BACKGROUND_COLOR)
        
        # ====================================================================
        # RENDER GLOW LAYERS (multiple passes for soft effect)
        # ====================================================================
        
        for glow_pass in range(3, 0, -1):
            for particle in particles:
                if particle.alpha > 0:
                    # Create glow surface with lower alpha
                    glow_alpha = int(particle.alpha * (0.3 / glow_pass))
                    
                    # Render "Melody" text
                    font_size = max(8, particle.size - glow_pass * 2)
                    font = pygame.font.Font(None, font_size)
                    
                    text_surf = font.render("Melody", True, particle.color)
                    text_surf.set_alpha(glow_alpha)
                    
                    # Rotate text slightly for visual interest
                    rotated = pygame.transform.rotate(text_surf, particle.rotation)
                    rect = rotated.get_rect(center=(int(particle.x), int(particle.y)))
                    
                    display.blit(rotated, rect)
        
        # ====================================================================
        # RENDER MAIN PARTICLES (bright pass)
        # ====================================================================
        
        for particle in particles:
            if particle.alpha > 0:
                font = pygame.font.Font(None, particle.size)
                text_surf = font.render("Melody", True, particle.color)
                text_surf.set_alpha(particle.alpha)
                
                rotated = pygame.transform.rotate(text_surf, particle.rotation)
                rect = rotated.get_rect(center=(int(particle.x), int(particle.y)))
                
                display.blit(rotated, rect)
        
        # ====================================================================
        # RENDER CENTER TEXT WITH GLOW
        # ====================================================================
        
        # Render center text glow layers
        love_text = "I LOVE YOU"
        glow_color_amount = int(100 + 50 * math.sin(frame * 0.05))
        glow_color = (glow_color_amount, glow_color_amount, 200)
        
        for glow_pass in range(4, 0, -1):
            glow_alpha = int(100 / glow_pass)
            glow_font_size = 80 + glow_pass * 4
            glow_font = pygame.font.Font(None, glow_font_size)
            glow_text = glow_font.render(love_text, True, glow_color)
            glow_text.set_alpha(glow_alpha)
            glow_rect = glow_text.get_rect(center=(center_x, center_y))
            display.blit(glow_text, glow_rect)
        
        # Render center text (bright)
        main_color = (200, 200, 255)
        main_text = center_font.render(love_text, True, main_color)
        main_text.set_alpha(220)
        main_rect = main_text.get_rect(center=(center_x, center_y))
        display.blit(main_text, main_rect)
        
        # ====================================================================
        # UPDATE DISPLAY AND FRAME TIMING
        # ====================================================================
        
        pygame.display.flip()
        clock.tick(FPS)
        frame += 1
    
    # Cleanup
    pygame.quit()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
