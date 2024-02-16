// import React, { Component } from 'react';
// import { Mesh } from 'three';
// import { Canvas, useFrame, extend, ReactThreeFiber } from '@react-three/fiber';
// import { OrbitControls } from '@react-three/drei';


// // Extend will make OrbitControls available as a JSX element called orbitControls for us
// extend({ OrbitControls });

// // TypeScript interface for props (if you have any props to pass in)
// interface BoxProps {
//   position: ReactThreeFiber.Vector3;
// }

// class Box extends Component<BoxProps> {
//   mesh = React.createRef<Mesh>(); // Use React.createRef and specify the type
//   frameId: number | null = null;

//   componentDidMount() {
//     this.startAnimation();
//   }

//   componentWillUnmount() {
//     this.stopAnimation();
//   }

//   startAnimation = () => {
//     if (!this.frameId) {
//       this.frameId = requestAnimationFrame(this.animate);
//     }
//   };

//   stopAnimation = () => {
//     if (this.frameId) {
//       cancelAnimationFrame(this.frameId);
//       this.frameId = null;
//     }
//   };

//   animate = () => {
//     if (this.mesh.current) {
//       this.mesh.current.rotation.x += 0.01;
//       this.mesh.current.rotation.y += 0.01;
//     }
//     this.frameId = requestAnimationFrame(this.animate);
//   };

//   render() {
//     return (
//       <mesh
//         {...this.props}
//         ref={this.mesh}
//         onClick={(event) => console.log('Mesh clicked')}
//         onPointerOver={(event) => console.log('Mouse over mesh')}
//         onPointerOut={(event) => console.log('Mouse out mesh')}>
//         <boxGeometry args={[1, 1, 1]} />
//         <meshStandardMaterial color={'orange'} />
//       </mesh>
//     );
//   }
// }

// const Scene = () => (
//     <Canvas>
//       <ambientLight intensity={0.5} />
//       <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
//       <pointLight position={[-10, -10, -10]} />
//       <Box position={[0, 0, 0]} />
//       <OrbitControls />
//     </Canvas>
//   );
  
// export default Scene;
