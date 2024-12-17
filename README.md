**Reformulated Argument Assuming Willow Exists and Efficiently Handles RCS**

1. **Premise: Willow’s Capabilities**  
   Assume Willow is a quantum device that can sample from the output distributions of complex random quantum circuits (RCS instances) both accurately and efficiently. “Efficiently” here means it can handle RCS instances of a size and complexity that would be classically intractable, and it can do so in time scales that render previously unsolvable problems feasible.

2. **Encoding SAT into RCS**  
   Consider any SAT instance \(\phi\) with \(n\) variables and \(m\) clauses. We construct a quantum circuit \(Q_\phi\) that:  
   - Uses \(n\) qubits to represent the variables.  
   - Initializes a uniform superposition over all \(2^n\) assignments.  
   - Includes controlled-phase operations or multi-controlled gates to impose a measurable bias against assignments that violate any clause of \(\phi\).  
   - Incorporates scrambling layers of gates to produce an RCS-like circuit structure.

   The result is a random quantum circuit whose output distribution, when measured, is not uniform. Assignments that satisfy \(\phi\) have constructive interference that increases their sampling probability, while invalid assignments are suppressed.

   This encoding is polynomial in the size of the SAT instance. Although detailed engineering might be needed, the principle is that each clause can be checked using a polynomial (or at worst, exponential but structured) number of gates—still far less than any brute-force search by classical means for large instances.

   Example code can be found in [reform.py](reform.py).

3. **Leveraging Willow**  
   Now we feed the constructed circuit \(Q_\phi\) into Willow. By assumption, Willow can handle RCS tasks quickly and accurately. It executes the circuit and produces measurement outcomes according to the encoded distribution.

   Because \(Q_\phi\) is constructed so that correct SAT solutions appear with higher probability than random guessing would yield, just a moderate number of samples from Willow should generate at least one satisfying assignment with a probability well above chance. If Willow can truly handle such circuits at scale, this step is tractable for large instances that would stymie classical algorithms.

4. **Extracting the SAT Solution**  
   After running \(Q_\phi\) on Willow, we analyze the collected measurement outcomes. We look for assignments that occur more frequently than one would expect from a uniform distribution. Among these more frequent assignments, at least one is highly likely to satisfy \(\phi\). Thus, we “read off” a correct SAT solution directly from the measurement data.

5. **Implication**  
   The argument doesn’t rely on any known polynomial-time classical algorithm. Instead, it exploits Willow’s assumed ability to solve large RCS instances efficiently. By showing that a generic SAT problem can be mapped to an RCS instance and then solved via RCS sampling, we conclude: If Willow truly provides a fast, accurate solution to RCS problems at scale, then it can be used to solve SAT problems that are otherwise intractable.

   While this does not constitute a proof that SAT can be solved in polynomial time (no complexity class collapse is proven), it is a practical demonstration that the existence of a powerful RCS-solving device like Willow can be leveraged to solve SAT. If one trusts the device’s capabilities—and if the encoding and extraction steps are manageable in practice—then SAT problems become “quantum solved” through RCS

   Any problem that can be reformulated as a single-shot RCS task—like SAT and, by reduction, many NP-complete problems—could be tackled rapidly. This has potentially transformative effects on fields relying on combinatorial optimization or large-scale constraint satisfaction, such as complex scheduling, supply chain logistics, and certain AI inference tasks. However, the benefit is limited to problems that can be encoded into a single pass of RCS. Willow cannot run iterative or adaptive algorithms directly; it provides only one-shot sampling from a fixed circuit. Thus, while static problems with well-defined, one-step RCS reductions may be solved quickly, problems requiring iterative refinement, feedback loops, or multiple rounds of computation may not gain the same advantage.

   Cryptosystems whose security relies on the hardness of single-shot, NP-complete problem instances may need re-evaluation. If their core security reduces to finding a solution to a single, static CSP that can be directly mapped to RCS, Willow’s capability would threaten their security assumptions. In contrast, cryptographic algorithms that rely on iterative hardness—such as elliptic curve cryptography (ECC), which depends on the discrete log problem—are not as easily cast into a one-shot RCS framework. These iterative problems require multiple steps or adaptive queries, which Willow’s single-shot approach does not accelerate. As a result, while certain “static” NP-based cryptographic schemes might need reconsideration, iterative or multi-round cryptographic algorithms remain less vulnerable to this specific quantum approach.

    - Knapsack-based cryptosystems  
    - Graph-based cryptosystems relying on NP-complete instances  
    - Subset-sum cryptographic schemes.

