import { OrbitControls } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import React from "react";
import { OrbitPath } from "./OrbitPath";
import { Asteroidbody } from "./AsteroidBody";


const scaleFactor = 1e9; // Example scale factor, adjust based on your needs

// Function to normalize/scale down positions
function normalizeVector(position: Position3D): Position3D {
  return {
    x: position.x / scaleFactor,
    y: position.y / scaleFactor,
    z: position.z / scaleFactor,
  };
}



export const Scene = () => {
    // Example asteroid data
    const asteroids = [
        {
            id: 1,
            position: { 'x': 328091412532.866, 'y': -115265600043.22685, 'z': 826642756.7659326 },
            orbitPoints: [{ 'x': 200777019622.20474, 'y': -216192185685.44592, 'z': 698349806.08945 }, { 'x': 391238881363.7621, 'y': 160095148073.9927, 'z': 592540975.800127 }, { 'x': 123223313761.30608, 'y': 388169056484.37537, 'z': -259704548.34203824 }, { 'x': -236150427703.19543, 'y': 107129249675.50444, 'z': -626926082.5460345 }] as Position3D[],

        },
        // Add more asteroids as needed
    ];

    const normalizedPosition = normalizeVector(asteroids[0].position);
    const normalizedOrbitPoints = asteroids[0].orbitPoints.map(normalizeVector);


    return (
        <Canvas
            style={{ height: "100vh", width: "100vw" }}
            camera={{ position: [0, 0, 300], fov: 75, near: 0.1, far: 10000 }}>

            <ambientLight intensity={0.5} />
            <pointLight position={[10, 10, 10]} />
            <React.Fragment>
                <Asteroidbody position={normalizedPosition} />
                <OrbitPath points={normalizedOrbitPoints} />
            </React.Fragment>
            <OrbitControls />
        </Canvas>
    );
};
