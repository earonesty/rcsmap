import itertools
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import transpile

def sat_eval(clauses, assignment):
    return all(any((assignment[var]==1 and not neg) or (assignment[var]==0 and neg)
               for var,neg in clause) for clause in clauses)

def sat_to_rcs(clauses, num_vars):
    num_clauses = len(clauses)

    # Use lists instead of range objects
    var_qubits = list(range(num_vars))
    clause_qubits = list(range(num_vars, num_vars+num_clauses))
    flag_qubit = num_vars+num_clauses

    qc = QuantumCircuit(num_vars+num_clauses+1, num_vars)

    # Step 1: Uniform superposition
    qc.h(var_qubits)

    # Initial "scramble" layer
    for i in range(num_vars+num_clauses+1):
        qc.rx((i+1)*0.3, i)
    for i in range(num_vars+num_clauses):
        qc.cx(i, i+1)
    for i in range(num_vars+num_clauses+1):
        qc.rz((i+1)*0.4, i)
    for i in range(num_vars+num_clauses,0,-1):
        qc.cx(i-1, i)

    # Encode clauses:
    # We'll mark clause ancillas as 1 if clause fails
    for ci, clause in enumerate(clauses):
        fail_controls = []
        for (v,neg) in clause:
            if not neg:
                # Clause fails if x_v=0, so flip if zero to enable fail detection
                qc.x(v)
                fail_controls.append(v)
            else:
                # Clause fails if x_v=1, use directly
                fail_controls.append(v)
        # Multi-controlled X onto clause ancilla
        qc.mcx(fail_controls, clause_qubits[ci])
        # Undo flips for non-negated literals
        for (v,neg) in clause:
            if not neg:
                qc.x(v)

    # If ANY clause fails, we apply a phase flip
    # Convert clause_qubits fail pattern into a single phase flip
    for cq in clause_qubits:
        qc.x(cq)
    qc.h(flag_qubit)
    qc.mcx(clause_qubits, flag_qubit)  # all clause_qubits as controls
    qc.h(flag_qubit)
    for cq in clause_qubits:
        qc.x(cq)

    # Another "scramble" layer
    for i in range(num_vars+num_clauses+1):
        qc.ry((i+1)*0.25, i)
    for i in range(num_vars+num_clauses):
        qc.cx(i, i+1)
    for i in range(num_vars+num_clauses+1):
        qc.rz((i+1)*0.1, i)
    for i in range(num_vars+num_clauses):
        qc.cx(i, i+1)

    # Measure variables
    qc.measure(var_qubits, var_qubits)
    return qc

# Example:
clauses = [
    [(0,False),(1,True),(2,False)],
    [(0,True),(3,False),(2,True)],
    [(1,False),(2,False),(3,True)]
]
num_vars = 4

qc = sat_to_rcs(clauses, num_vars)
sim = AerSimulator()
qc_t = transpile(qc, sim)
res = sim.run(qc_t, shots=2000).result()
counts = res.get_counts()

solutions = []
for assignment,count in counts.items():
    bits = [int(b) for b in assignment[::-1]]
    assign_dict = {i:bits[i] for i in range(num_vars)}
    if sat_eval(clauses, assign_dict):
        solutions.append((assignment,count))

# Basic assertion
assert len(solutions) > 0, "No satisfying assignment found."
