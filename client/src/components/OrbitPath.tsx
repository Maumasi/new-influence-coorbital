import React from 'react';
import { CatmullRomCurve3, Vector3, BufferGeometry, LineBasicMaterial, LineLoop } from 'three';
import { useThree } from '@react-three/fiber';

interface OrbitPathProps {
    points: Position3D[];
}

export const OrbitPath: React.FC<OrbitPathProps> = ({ points }) => {
    const { scene } = useThree();

    // Convert points from {x, y, z} to Vector3
    const vectors = points.map(point => new Vector3(point.x, point.y, point.z));

    // Create a smooth curve through the points and close it
    const curve = new CatmullRomCurve3(vectors, true, 'catmullrom', 0.5);

    // Get a set of points to define the geometry of the curve
    const pointsSmooth = curve.getPoints(50); // Increase number of points for a smoother curve

    // Create the curve geometry and material
    const geometry = new BufferGeometry().setFromPoints(pointsSmooth);
    const material = new LineBasicMaterial({ color: "black", linewidth: 1 });

    // Remove previous orbit from the scene if it exists
    const previousOrbit = scene.getObjectByName('orbitPath');
    if (previousOrbit) {
        scene.remove(previousOrbit);
    }

    // Create the orbit line using LineLoop for a closed path
    const orbitLine = new LineLoop(geometry, material);
    orbitLine.name = 'orbitPath';

    // Add the orbit line to the scene
    scene.add(orbitLine);

    return null; // This component does not render anything itself
};
