# Quantum Poisson Surface Reconstruction

A computational study of **Poisson Surface Reconstruction (PSR)** in 2D and 3D, combining classical numerical methods with quantum approaches to the underlying Poisson solver.

The project investigates the complete reconstruction pipeline, from oriented point samples and vector-field construction through to Poisson solving and surface extraction. The quantum component focuses on replacing the classical Poisson linear-system solver with a quantum formulation, followed by sensitivity analysis across different geometries.

## Overview

Poisson Surface Reconstruction converts a set of oriented points into an implicit representation of a surface.

Given scan points \(p_i\) and corresponding normals \(n_i\), the method first constructs a vector field over a regular grid. The divergence of this field is then used as the source term of a Poisson equation:

$$
\Delta \chi = \nabla \cdot V
$$

where:

* \(V\) is the vector field constructed from the input normals,
* \(\chi\) is the implicit indicator function,
* \(\Delta\) is the Laplacian operator.

After discretisation, the Poisson problem can be expressed as a linear system,

$$
A\chi=b.
$$

This project investigates both classical and quantum approaches to solving this problem.

## Reconstruction Pipeline

The classical reconstruction algorithm follows the pipeline:

```text
Oriented Scan Points
        │
        ▼
Vector Field Construction
        │
        │  Smoothing Kernel
        ▼
Regular Grid Vector Field V
        │
        ▼
Divergence ∇ · V
        │
        ▼
Poisson Equation
        │
        ▼
      Δχ = ∇ · V
        │
        ▼
Poisson Solver
        │
   ┌────┴─────┐
   │          │
Classical   Quantum
   │          │
   └────┬─────┘
        ▼
Implicit Function χ
        │
        ▼
Interpolation at Scan Points
        │
        ▼
Isovalue Estimation
        │
        ▼
Reconstructed Surface
```

# Sensitivity Analysis

A significant part of the project is the sensitivity analysis performed across different geometries.

Rather than evaluating the method on a single surface, multiple geometries are considered to investigate how the reconstruction and Poisson solver respond to changes in the underlying problem.

The analysis examines factors such as:

* geometry,
* grid resolution,
* smoothing kernals,
* discretisation,
* Poisson-system properties,
* reconstruction error,
* and differences between classical and quantum solutions.

The general experimental workflow is:

$$
\text{Geometry}
\rightarrow
\text{Vector Field}
\rightarrow
\text{Divergence}
\rightarrow
A\chi=b
\rightarrow
\text{Solver}
\rightarrow
\text{Reconstruction}
\rightarrow
\text{Error Analysis}.
$$

This allows the behaviour of the reconstruction to be studied systematically rather than relying on a single example.

# Experiments

The experiments are organised around three main questions:

### 1. Reconstruction

Can the Poisson formulation accurately reconstruct different 2D and 3D geometries?

### 2. Quantum solution

How does a quantum approach to the Poisson linear system compare with the classical solution?

### 3. Sensitivity

How does the reconstruction change as the geometry, discretisation, or other numerical parameters are varied?

Results include reconstructed geometries, error measurements, solver comparisons, and sensitivity plots.

# Project Structure

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
├── notebooks/
│   ├── 2D/
│   └── 3D/
│
├── results/
│   ├── figures/
│   ├── reconstructions/
│   └── sensitivity/
│
├── src/
│   ├── poisson/
│   ├── reconstruction/
│   ├── quantum/
│   └── analysis/
│
└── README.md
```

# Packages

The project uses:

* **Python**
* **NumPy**
* **SciPy**
* **Matplotlib**
* **Qiskit**
* **Qiskit Aer**

# Key Contributions

The project combines several areas of computational science:

* **Poisson Surface Reconstruction**
* **Numerical PDEs**
* **Fourier-based Poisson solving**
* **Numerical linear algebra**
* **Quantum linear-system algorithms**
* **Computational geometry**
* **Sensitivity and error analysis**

The main contribution is an experimental framework for investigating how a quantum Poisson solver can be incorporated into a surface-reconstruction pipeline and how its behaviour changes across different geometries and problem configurations.

# Limitations and Future Work

The current implementation provides a framework for investigating quantum Poisson solving, but several challenges remain before such an approach could provide practical advantages over established classical methods.

Potential extensions include:

* a quantum algorithm for screened PSR,
* a quantum algorithm for a octree-based PSR algorithm,
* noise and error mitigation,
* alternative quantum linear-system algorithms like a polynomial approximation algorithm,
* more extensive geometric datasets,
* and end-to-end resource comparisons between classical and quantum approaches.

# Summary

This project investigates **Poisson Surface Reconstruction through both classical and quantum approaches**.

Starting from oriented point samples, the method constructs a smoothed vector field, calculates its divergence, solves the resulting Poisson equation, and extracts an implicit surface.

The classical solver uses a **Fourier-domain solution of the Poisson equation**, while the quantum implementation investigates a quantum approach to the underlying linear-system problem.

The methodology is evaluated in both **2D and 3D**, with sensitivity analysis across multiple geometries to study reconstruction accuracy and solver behaviour.

The project therefore sits at the intersection of:

$$
\boxed{
\text{Computational Geometry}
+
\text{PDEs}
+
\text{Numerical Linear Algebra}
+
\text{Quantum Computing}
}
$$

## Author

**Avinash Pothuri**

I would like to thank Dr Eky Febrianto for supervising me through this project
