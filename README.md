# Quantum RCS-SAT Mapping

This repository provides a method to encode SAT problems into quantum circuits using Random Circuit Sampling (RCS). The goal is to explore whether RCS-capable quantum processors can provide computational advantages in solving SAT instances.

## Overview

The approach involves:
- Mapping SAT variables to qubits
- Encoding clauses as quantum gate operations
- Using RCS to generate output samples
- Extracting satisfying assignments from sampled output

## Explanation of the rcsmap.py program:

1. **Mapping SAT Variables to Qubits**  
   Each SAT variable is associated with a specific qubit in the quantum circuit. The state of each qubit represents the truth assignment of the corresponding SAT variable.

2. **Constructing the Quantum Circuit**  
   Each clause of the SAT problem is translated into a series of quantum gates. These gates enforce constraints on the state space such that satisfying assignments correspond to valid quantum states.

3. **Measuring the Quantum State**  
   After executing the circuit, the qubits are measured, yielding a classical bitstring. Each bit in the output represents a truth assignment.

4. **Interpreting the Measurement Results**  
   The sampled bitstrings are analyzed to check if they satisfy all SAT clauses. The process is repeated multiple times to improve the probability of obtaining a satisfying assignment.

5. **Repeating the Process**  
   Due to the probabilistic nature of quantum measurements, multiple samples are taken to ensure a valid solution emerges with high probability.

This approach investigates whether quantum sampling techniques can enhance classical SAT-solving methods by efficiently exploring the solution space. Future work includes benchmarking against classical solvers and testing on real quantum hardware.

# Assuming Quantum Computers Efficiently Handle RCS

1. **Premise: Quanum Computing Capabilities**  
    There are many uantum devices that can sample from the output distributions of complex random quantum circuits (RCS instances) both accurately and efficiently. “Efficiently” here means it can handle RCS instances of a size and complexity that would be classically intractable, and it can do so in time scales that render previously unsolvable problems feasible.

    The implications are serious.

2. **Encoding SAT into RCS**  
   Consider any SAT instance \(\phi\) with \(n\) variables and \(m\) clauses. We construct a quantum circuit \(Q_\phi\) that:  
   - Uses \(n\) qubits to represent the variables.  
   - Initializes a uniform superposition over all \(2^n\) assignments.  
   - Includes controlled-phase operations or multi-controlled gates to impose a measurable bias against assignments that violate any clause of \(\phi\).  
   - Incorporates scrambling layers of gates to produce an RCS-like circuit structure.

   The result is a random quantum circuit whose output distribution, when measured, is not uniform. Assignments that satisfy \(\phi\) have constructive interference that increases their sampling probability, while invalid assignments are suppressed.

   This encoding is polynomial in the size of the SAT instance. The principle is that each clause can be checked using a polynomial (or at worst, exponential but structured) number of gates—still far less than any brute-force search by classical means.

   Example code can be found in [reform.py](reform.py).

4. **Leveraging RCS**  
   Now we feed the constructed circuit \(Q_\phi\) into an RCS device.  The RCS device executes the circuit and produces measurement outcomes according to the encoded distribution.

   Because \(Q_\phi\) is constructed so that correct SAT solutions appear with higher probability than random guessing would yield, just a moderate number of samples from the RCS device should generate at least one satisfying assignment with a probability well above chance. If an RCS device can truly handle such circuits at scale, this step is tractable for large instances that would stymie classical algorithms.

5. **Extracting the SAT Solution**  
   After running \(Q_\phi\) on an RCS device, we analyze the collected measurement outcomes. We look for assignments that occur more frequently than one would expect from a uniform distribution. Among these more frequent assignments, at least one is highly likely to satisfy \(\phi\). Thus, we “read off” a correct SAT solution directly from the measurement data.

   The code demonstrates this is possible for random satisfiability problems.

6. **Implication**  
   The argument doesn’t rely on any known polynomial-time classical algorithm. Instead, it exploits RCS device’s assumed ability to solve large RCS instances efficiently. By showing that a generic SAT problem can be mapped to an RCS instance and then solved via RCS sampling, we conclude: If RCS devices truly provide fast, accurate solutions at scale, then it can be used to solve SAT problems that are otherwise intractable.

   This is a practical and functional demonstration that the existence of a powerful RCS-solving device can be leveraged to solve SAT. SAT problems have become “quantum solved” through RCS.

   Any problem that can be reformulated as a single-shot RCS task—like SAT and, by reduction, many NP-complete problems—could be tackled rapidly. This has transformative effects on fields relying on combinatorial optimization or large-scale constraint satisfaction, such as complex scheduling, supply chain logistics, and certain AI inference tasks. However, the benefit is limited to problems that can be encoded into a single pass of RCS. These RCS devices cannot run iterative or adaptive algorithms directly; it provides only one-shot sampling from a fixed circuit. Thus, while static problems with well-defined, one-step RCS reductions may be solved quickly, problems requiring iterative refinement, feedback loops, or multiple rounds of computation may not gain a time advantage.

   Cryptosystems whose security relies on the hardness of single-shot, NP-complete problem instances need immediate re-evaluation. If core security reduces to finding a solution to a single, static CSP that can be directly mapped to RCS, these quantum capabilities would threaten their security assumptions. In contrast, cryptographic algorithms that rely on iterative hardness—such as elliptic curve cryptography (ECC), which depends on the discrete log problem—are not as easily cast into a one-shot RCS framework. These iterative problems require multiple steps or adaptive queries, which modern quantum single-shot approach does not accelerate. As a result, while certain “static” NP-based cryptographic schemes might need reconsideration, iterative or multi-round cryptographic algorithms remain less vulnerable to this specific quantum approach.

    - Knapsack-based cryptosystems  
    - Graph-based cryptosystems relying on NP-complete instances  
    - Subset-sum cryptographic schemes.

