# Quantum Poisson Surface Reconstruction

# Quantum Poisson Surface Reconstruction

A computational study of **Poisson Surface Reconstruction (PSR)** in 2D and 3D, together with quantum formulations of the underlying **Poisson linear-system solver** and sensitivity analysis across different geometries.

The project investigates how classical and quantum approaches to solving the Poisson equation can be applied to surface reconstruction problems, and how reconstruction quality and solver behaviour change under different geometric configurations.

---

## Overview

Poisson Surface Reconstruction is a widely used technique for reconstructing an implicit surface from oriented point samples. At its core, the reconstruction problem can be formulated as a **Poisson equation**, which is discretised into a linear system.

This project explores the problem at three levels:

* **Classical Poisson Surface Reconstruction**

  * 2D reconstruction
  * 3D reconstruction
  * Numerical solution of the resulting Poisson system

* **Quantum Poisson Solving**

  * Quantum formulations of the Poisson linear-system solving component
  * Application to both 2D and 3D reconstruction problems
  * Comparison with the corresponding classical approach

* **Sensitivity Analysis**

  * Experiments across multiple geometries
  * Investigation of reconstruction accuracy and solver behaviour
  * Analysis of how changes in geometry and problem parameters affect the solution

The overall workflow is:

```text
Point / Geometric Data
        │
        ▼
Surface / Vector Field Representation
        │
        ▼
Poisson Equation
        │
        ▼
Discretisation
        │
        ▼
Linear System
   ┌────┴────┐
   │         │
   ▼         ▼
Classical   Quantum
 Solver      Solver
   │         │
   └────┬────┘
        ▼
Reconstructed Surface
        │
        ▼
Sensitivity Analysis
```

---

## Objectives

The main objectives of the project are:

1. Implement Poisson-based surface reconstruction in **2D and 3D**.
2. Formulate the resulting Poisson problem as a linear system.
3. Investigate a **quantum approach to solving the Poisson linear system**.
4. Compare classical and quantum solution approaches.
5. Study the sensitivity of the reconstruction to different geometries and numerical parameters.
6. Investigate the practical challenges involved in applying quantum linear-system methods to computational geometry problems.

---

# 1. Poisson Surface Reconstruction

## 1.1 Mathematical formulation

Poisson surface reconstruction can be expressed through the relationship

$$
\nabla \cdot \nabla \chi = \nabla \cdot V,
$$

or equivalently,

$$
\Delta \chi = \nabla \cdot V,
$$

where:

* \(\chi\) is the implicit indicator function representing the reconstructed surface,
* \(V\) is a vector field constructed from the oriented input data,
* \(\Delta\) is the Laplacian operator.

The resulting Poisson equation is discretised to obtain a linear system of the form

$$
A x = b.
$$

Solving this system provides the information required to recover the reconstructed surface.

---

# 2. 2D Reconstruction

The first part of the project considers the Poisson reconstruction problem in **two dimensions**.

The 2D implementation provides a controlled environment for studying:

* discretisation of the Poisson equation,
* construction of the linear system,
* reconstruction accuracy,
* numerical stability,
* and the behaviour of the corresponding quantum solver.

Different geometries are used to investigate how the reconstruction responds to changes in the input geometry.

### Example geometries

The experiments include multiple geometric configurations to test the solver under different conditions.

Typical analysis includes:

* reconstructed geometry,
* reconstruction error,
* solution behaviour,
* sensitivity to perturbations,
* and comparison between classical and quantum approaches.

---

# 3. 3D Reconstruction

The project extends the same methodology to **three-dimensional surface reconstruction**.

The 3D problem introduces additional computational and numerical considerations because the discretised Poisson system becomes significantly larger.

The 3D pipeline can be summarised as:

```text
3D Point Cloud
      │
      ▼
Oriented Normals
      │
      ▼
Vector Field
      │
      ▼
Poisson Equation
      │
      ▼
Discretised Linear System
      │
      ▼
       Ax = b
      │
   ┌──┴──┐
   ▼     ▼
Classical Quantum
Solver    Solver
   │       │
   └───┬───┘
       ▼
Reconstructed Surface
```

The 3D experiments are particularly useful for examining how the methods behave as the dimensionality and size of the underlying problem increase.

---

# 4. Quantum Poisson Solver

A central component of the project is the development of a **quantum formulation of the Poisson solver**.

After discretisation, the Poisson equation takes the form

$$
Ax=b.
$$

This is a linear-system problem, making it relevant to quantum algorithms for linear algebra.

The quantum component therefore focuses primarily on the **Poisson solver itself**, rather than attempting to replace the entire surface-reconstruction pipeline with a quantum algorithm.

The general quantum workflow is:

```text
Poisson Problem
      │
      ▼
Discretisation
      │
      ▼
     Ax = b
      │
      ▼
Quantum Linear-System Formulation
      │
      ▼
Quantum State / Solution
      │
      ▼
Extract Relevant Quantities
      │
      ▼
Surface Reconstruction
```

The project investigates how the quantum formulation behaves for both the 2D and 3D Poisson problems.

---

# 5. Classical vs Quantum Approach

An important aspect of the project is distinguishing between the mathematical formulation of the problem and the method used to solve the resulting linear system.

| Component            | Classical Approach         | Quantum Approach                   |
| -------------------- | -------------------------- | ---------------------------------- |
| Geometry             | Classical                  | Classical                          |
| Poisson formulation  | Classical                  | Classical                          |
| Discretisation       | Classical                  | Classical                          |
| Linear system        | \(Ax=b\)                   | \(Ax=b\)                           |
| Linear-system solver | Classical numerical method | Quantum linear-system method       |
| Reconstruction       | Classical post-processing  | Quantum solution + post-processing |
| Sensitivity analysis | ✓                          | ✓                                  |

This makes it possible to investigate the potential role of quantum linear-system algorithms within an otherwise classical computational-geometry pipeline.

---

# 6. Sensitivity Analysis

A major component of the project is the **sensitivity analysis** performed across different geometries.

The purpose of this analysis is to determine how changes in the underlying problem affect the reconstructed solution.

The experiments consider different geometric configurations and examine quantities such as:

* reconstruction accuracy,
* numerical error,
* stability,
* changes in the Poisson system,
* solver behaviour,
* and differences between classical and quantum solutions.

Conceptually:

$$
\text{Geometry}
\rightarrow
\text{Poisson System}
\rightarrow
\text{Solver}
\rightarrow
\text{Reconstruction}
\rightarrow
\text{Error}
$$

By varying the geometry and relevant parameters, the project examines the sensitivity of each stage of this pipeline.

---

# 7. Experimental Geometries

The sensitivity experiments are performed across multiple geometries in both 2D and 3D.

This allows the project to investigate whether solver behaviour is consistent across different types of surfaces rather than being specific to a single example.

For each geometry, the analysis can include:

### Input

* Point locations
* Surface geometry
* Orientation / normal information
* Discretisation parameters

### Solver

* Poisson matrix \(A\)
* Right-hand side \(b\)
* Condition / numerical properties of the system
* Classical solution
* Quantum solution

### Output

* Reconstructed geometry
* Reconstruction error
* Difference between classical and quantum solutions
* Sensitivity to perturbations

---

# 8. Results and Analysis

The results are organised around three main questions:

### 1. Can the Poisson reconstruction problem be formulated consistently in 2D and 3D?

The classical implementations provide the baseline against which the quantum approach can be evaluated.

### 2. Can the Poisson linear system be treated using a quantum linear-system approach?

The quantum implementation investigates the practical steps required to encode and solve the discretised system using quantum methods.

### 3. How sensitive is the reconstruction to the underlying geometry and numerical parameters?

The sensitivity analysis provides insight into the robustness of both approaches and highlights how the structure of the geometry influences the resulting Poisson system.

---

# 9. Project Structure

The repository is organised approximately as follows:

```text
.
├── 2D/
│   ├── classical/
│   ├── quantum/
│   └── sensitivity/
│
├── 3D/
│   ├── classical/
│   ├── quantum/
│   └── sensitivity/
│
├── data/
│   └── geometries/
│
├── results/
│   ├── figures/
│   ├── reconstructions/
│   └── analysis/
│
├── notebooks/
│   ├── 2D/
│   └── 3D/
│
├── src/
│   ├── poisson/
│   ├── reconstruction/
│   ├── quantum/
│   └── analysis/
│
└── README.md
```

*The exact structure may differ depending on the implementation.*

---

# 10. Technologies

The project uses computational and quantum-computing tools for numerical experimentation.

Potential components include:

* **Python**
* **NumPy**
* **SciPy**
* **Matplotlib**
* **[Quantum computing framework used in the project]**
* Numerical linear algebra
* Computational geometry
* Partial differential equations

---

# 11. Key Concepts

This project brings together several areas of computational science:

### Computational Geometry

Representation and reconstruction of geometric surfaces from sampled data.

### Partial Differential Equations

The reconstruction problem is formulated using the Poisson equation,

$$
\Delta \chi = \nabla \cdot V.
$$

### Numerical Linear Algebra

Discretisation produces a linear system,

$$
Ax=b,
$$

which must be solved accurately and efficiently.

### Quantum Computing

Quantum linear-system methods are investigated as an alternative approach to solving the Poisson system.

### Numerical Sensitivity

The behaviour of the reconstruction is studied under changes to geometry and numerical parameters.

---

# 12. Limitations

The quantum results should be interpreted in the context of the implementation and simulation environment.

In particular, a quantum formulation of the linear-system solver does not automatically imply an end-to-end quantum speedup for Poisson surface reconstruction.

Practical considerations include:

* state preparation,
* encoding the matrix and right-hand side,
* quantum circuit depth,
* measurement and readout,
* noise in hardware implementations,
* classical preprocessing,
* and the cost of extracting useful information from the quantum state.

Therefore, the project focuses on **investigating the quantum formulation and its behaviour**, rather than assuming a practical computational advantage over classical Poisson solvers.

---

# 13. Future Work

Possible extensions include:

* Scaling the experiments to larger 3D point clouds.
* Investigating sparse quantum linear-system methods.
* Testing the algorithms on actual quantum hardware.
* Studying the effects of noise and error mitigation.
* Improving state-preparation methods.
* Comparing different quantum linear-system algorithms.
* Investigating preconditioning strategies.
* Measuring the effect of matrix condition number on quantum solver performance.
* Exploring end-to-end quantum surface reconstruction.
* Extending the sensitivity analysis to noisy and incomplete point clouds.

---

# 14. Summary

This project investigates the intersection of **Poisson surface reconstruction and quantum computing**.

The work progresses from classical numerical reconstruction in **2D and 3D**, to quantum formulations of the underlying **Poisson linear-system solver**, followed by a systematic **sensitivity analysis across different geometries**.

The central computational problem is:

$$
\boxed{Ax=b}
$$

where the matrix \(A\) originates from the discretised Poisson equation.

By studying both classical and quantum approaches to this system, the project provides a framework for examining where quantum linear-algebra techniques may fit within computational geometry and PDE-based reconstruction workflows.

---

## Author

**[Your Name]**

[GitHub Profile](https://github.com/[username])

---

## Citation

If you use this project or its results, please cite:

```bibtex
@misc{poisson_quantum_reconstruction,
  author = {[Your Name]},
  title  = {Quantum Poisson Surface Reconstruction},
  year   = {2026},
  url    = {https://github.com/[username]/[repository]}
}
```
