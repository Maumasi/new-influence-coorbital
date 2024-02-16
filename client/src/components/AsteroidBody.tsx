import React from 'react';
import { Sphere } from '@react-three/drei';
import { Vector3 } from '@react-three/fiber';

// var position = {'x': 328091412532.866, 'y': -115265600043.22685, 'z': 826642756.7659326}
interface AsteroidBodyProps {
    position: Position3D;
}

export const Asteroidbody: React.FC<AsteroidBodyProps> = ({ position }) => {

  return (
    <Sphere position={[position.x, position.y, position.x]} args={[50, 16, 16]} > {/* args are [radius, widthSegments, heightSegments] */}
      <meshStandardMaterial color={'grey'} />
    </Sphere>
  );
};
