import pygame
import numpy as np
from numba import njit

# Initialize pygame
pygame.init()

# Mouse tracking variables
mouse_pressed = False
mouse_position = (0, 0)
last_mouse_position = (0, 0)


# Set up the screen dimensions
screen_width, screen_height = 1024, 768
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Gravitational constant, softening factor, and friction
G = 6.674e-5
softening_factor = 35
friction_factor = 0.9995  # Slightly reduce velocity over time
heat_gain_rate = 0.05 # New factor to control heat gain rate
cooling_factor = 0.8  # Adjusted cooling factor


def lerp_color(color1, color2, t):
    """ Linearly interpolate between two colors """
    return tuple(int(a + (b - a) * t) for a, b in zip(color1, color2))

def heat_to_color(heat):
    max_heat = 3
    normalized_heat = min(heat / max_heat, 1)

    # Define color ranges
    cold_color = (10,10,10)  # Dark grey
    warm_color = (255, 0, 0)   # Red
    hot_color = (255, 128, 0)  # Orange
    very_hot_color = (255, 255, 0)  # Yellow

    if normalized_heat < 0.7:
        # Interpolate between cold_color and warm_color
        return lerp_color(cold_color, warm_color, normalized_heat / 0.7)
    elif normalized_heat < 0.8:
        # Interpolate between warm_color and hot_color
        t = (normalized_heat - 0.7) / (0.8 - 0.7)
        return lerp_color(warm_color, hot_color, t)
    elif normalized_heat < 0.95:
        # Interpolate between hot_color and very_hot_color
        t = (normalized_heat - 0.8) / (0.95 - 0.8)
        return lerp_color(hot_color, very_hot_color, t)
    else:
        return very_hot_color

# Function to calculate glow properties
def calculate_glow_properties(heat):
    max_heat = 3  # Adjust this based on the maximum expected heat value
    normalized_heat = min(heat / max_heat, 1)
    base_glow_size = 10  # Base size for glow, adjust as needed

    glow_size = int(base_glow_size * normalized_heat)

    # Alpha should increase with heat. Fully transparent at 0 heat and less transparent at higher heat
    min_alpha = 0  # Fully transparent
    max_alpha = 32  # Semi-transparent
    alpha = int(min_alpha + (max_alpha - min_alpha) * normalized_heat)

    return glow_size, alpha


@njit
def calculate_forces_and_heat(particles, G, softening_factor, screen_width, screen_height, heat_gain_rate, cooling_factor):
    forces = np.zeros((len(particles), 2))
    for i in range(len(particles)):
        net_heat_effect = 0  # Net effect of forces for heat change

        for j in range(len(particles)):
            if i != j:
                dx = particles[j][0] - particles[i][0]
                dy = particles[j][1] - particles[i][1]
                dx = dx - screen_width * round(dx / screen_width)
                dy = dy - screen_height * round(dy / screen_height)

                r = np.sqrt(dx**2 + dy**2 + softening_factor**2)
                F = G * particles[i][2] * particles[j][2] / r**2

                forces[i][0] += F * dx / r
                forces[i][1] += F * dy / r

                # Accumulate the magnitude of the force for heat effect
                force_magnitude = np.sqrt((F * dx / r)**2 + (F * dy / r)**2)
                net_heat_effect += force_magnitude / particles[i][2]

        # Heating or cooling based on net heat effect
        if net_heat_effect > heat_gain_rate:
            particles[i][5] += net_heat_effect * heat_gain_rate  # Heat gain
            particles[i][5] *= 0.99  # Heat loss
        else:
            particles[i][5] *= cooling_factor  # Heat loss

    return forces

# Create particles with an additional field for heat
particles = np.array([[np.random.uniform(0, 1024), np.random.uniform(0, 768),
                       np.random.uniform(4e3, 1e5),  # Mass
                       np.random.uniform(-0.1, 0.1),  # Velocity x
                       np.random.uniform(-0.1, 0.1),  # Velocity y
                       0.0]  # Initial heat
                      for _ in range(500)])

# Function to create a surface with a glow effect
def create_glow_surface(radius, color):
    glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(glow_surface, color, (radius, radius), radius)
    return glow_surface

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False

    # Update mouse positions
    last_mouse_position = mouse_position
    mouse_position = pygame.mouse.get_pos()

    if mouse_pressed:
        # Calculate mouse movement vector for momentum
        mouse_dx, mouse_dy = mouse_position[0] - last_mouse_position[0], mouse_position[1] - last_mouse_position[1]

        # Create a new particle at the mouse position with momentum
        new_particle = [mouse_position[0], mouse_position[1],
                        np.random.uniform(4e3, 1e5),  # Mass
                        mouse_dx * 0.1,  # Velocity x influenced by mouse movement
                        mouse_dy * 0.1,  # Velocity y influenced by mouse movement
                        0.0]  # Initial heat
        particles = np.append(particles, [new_particle], axis=0)

    screen.fill((0, 0, 0))
    forces = calculate_forces_and_heat(particles, G, softening_factor, screen_width, screen_height, heat_gain_rate, cooling_factor)
    
      
    for i, particle in enumerate(particles):
        # Update velocities based on forces and apply friction
        particle[3] += forces[i][0] / particle[2]  # vx
        particle[4] += forces[i][1] / particle[2]  # vy
        particle[3] *= friction_factor
        particle[4] *= friction_factor

        # Update positions based on velocities
        particle[0] += particle[3]  # x
        particle[1] += particle[4]  # y

        # Wraparound effect
        particle[0] %= screen_width
        particle[1] %= screen_height

        # Calculate particle color and glow size based on heat
        particle_color = heat_to_color(particles[i][5])
        glow_size, alpha = calculate_glow_properties(particles[i][5])

        # Calculate the particle size
        particle_size = int(np.sqrt(particle[2]) / 50)

        # Draw glow effect with dynamic size and color
        if glow_size > 0:
            total_glow_size = glow_size + particle_size
            glow_color = (*particle_color, alpha)  # Adjust alpha for desired transparency
            glow_surface = create_glow_surface(total_glow_size, glow_color)
            # Adjust the position to center the particle in the glow
            glow_position = (int(particle[0]) - total_glow_size, int(particle[1]) - total_glow_size)
            screen.blit(glow_surface, glow_position)

        # Draw the particle
        pygame.draw.circle(screen, particle_color, (int(particle[0]), int(particle[1])), particle_size)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
