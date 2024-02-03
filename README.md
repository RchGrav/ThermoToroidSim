# ThermoToroidSim
![animation](anim.gif)

## Description
ThermoToroidSim is a playful yet insightful physics simulation, a toy project that amalgamates gravitational dynamics, thermal behavior, and computational acceleration using Numba. While simplistic in its approach, it embodies core concepts of particle coalescence, thermal dynamics from gravitational compression, friction, and particle interaction in a 2D toroidal playfield.

## Key Concepts Explored
- **Numba Acceleration:** Utilizes Numba, a JIT compiler, to significantly speed up the computation of forces and heat exchange between particles, demonstrating the benefits of optimized Python code for scientific computation.
- **Particle Coalescence and Thermal Dynamics:** Initially places 500 particles randomly, simulating a very basic form of particle coalescence and thermal dynamics influenced by gravitational interactions and friction.
- **Toroidal Playfield Design:** The screen is conceptualized as being wrapped into a tube, with the ends connected, forming a toroidal field. This unique design overcomes edge effects, allowing gravity to act seamlessly across this continuous plane.
- **Gravitational and Heat Interactions:** Showcases how particles interact under gravity and how their motion and collisions result in changes in heat, visualized through color changes.

## Design Choices
- **Simplicity and Modifiability:** The program is deliberately kept simple and open for modifications. Users can tweak constants, add features, or modify the simulation rules.
- **Visualization and Interaction:** Prioritizes real-time visual feedback and user interaction, making it an engaging tool for exploring basic physics concepts.

## How to Use
- **Basic Operation:** The simulation starts with 500 randomly placed particles. The motion and interactions among these particles are governed by the defined physical laws.
- **Interactivity:** Users can add particles by clicking, seeing immediate effects on the system's dynamics.
- **Modification:** Feel free to experiment with the code. Adjust constants, alter the physics rules, or add new features to explore different aspects of the simulation.

## Installation and Running
Requires Python with Pygame, Numpy, and Numba. Run the simulation by executing the Python script. It's a compact, all-in-one Python program, easy to run and modify.

## Contributing
This project is open for contributions. Whether it's extending the simulation, enhancing performance, or improving visualization, your contributions are welcome.

## License
Open-source under the [MIT License](LICENSE).

## Acknowledgments
- Community contributions to Python, Pygame, Numpy, and Numba, making such simulations accessible and performant.
