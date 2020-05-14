from qiskit import *


class computer_ai:
    def __init__(self, board):
        self.move = 0
        self.num_t_gates = [0] * 9
        self.board = board
        self.board1 = [0] * 9
        for i in range(len(board)):
            if board[i] != " ":
                self.board1[i] = 1

    def best_move(self):

        self.num_t_gates = [0] * 9
        q = QuantumRegister(9)
        c = ClassicalRegister(9)
        qc = QuantumCircuit(q, c)  # Create a Quantum Circuit acting on the q register

        for index, move in enumerate(self.board1):

            if move:
                qc.x(q[index])
            else:
                qc.h(q[index])
                t_count = 0

                # first element in the row
                if index % 3 == 0:

                    # two same in a row
                    if self.board1[index + 1] and self.board1[index + 2] and self.board1[index + 1] == self.board1[index + 2]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    # only one of the spaces is occupied (or is xor, but they both have to explicitly be bools)
                    elif bool(self.board1[index + 1]) or bool(self.board1[index + 2]):
                        qc.t(q[index])
                        t_count += 1

                # middle element in the row
                if index % 3 == 1:
                    if self.board1[index + 1] and self.board1[index - 1] and self.board1[index + 1] == self.board1[index - 1]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif bool(self.board1[index + 1]) or bool(self.board1[index - 1]):
                        qc.t(q[index])
                        t_count += 1

                # last element in the row
                if index % 3 == 2:
                    if self.board1[index - 1] and self.board1[index - 2] and self.board1[index - 1] == self.board1[index - 2]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif bool(self.board1[index - 1]) or bool(self.board1[index - 2]):
                        qc.t(q[index])
                        t_count += 1

                # check column first row
                if index / 3 < 1:
                    if self.board1[index + 3] and self.board1[index + 6] and self.board1[index + 3] == self.board1[index + 6]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif bool(self.board1[index + 3]) or bool(self.board1[index + 6]):
                        qc.t(q[index])
                        t_count += 1

                # middle row
                if 2 > index / 3 >= 1:
                    if self.board1[index - 3] and self.board1[index + 3] and self.board1[index - 3] == self.board1[index + 3]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif bool(self.board1[index - 3]) or bool(self.board1[index + 3]):
                        qc.t(q[index])
                        t_count += 1

                # bottom row
                if index / 3 >= 2:
                    if self.board1[index - 3] and self.board1[index - 6] and self.board1[index - 3] == self.board1[index - 6]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif bool(self.board1[index - 3]) or bool(self.board1[index - 6]):
                        qc.t(q[index])
                        t_count += 1

                self.num_t_gates[index] = t_count

        # hard code in the diagonals
        if self.board1[0] and self.board1[0] == self.board1[4]:
            qc.t(q[8])
            qc.t(q[8])
            qc.t(q[8])
            self.num_t_gates[8] += 3
        if self.board1[0] and self.board1[0] == self.board1[8]:
            qc.t(q[4])
            qc.t(q[4])
            qc.t(q[4])
            self.num_t_gates[4] += 3
        if self.board1[4] and self.board1[4] == self.board1[8]:
            qc.t(q[0])
            qc.t(q[0])
            qc.t(q[0])
            self.num_t_gates[0] += 3
        if self.board1[2] and self.board1[2] == self.board1[4]:
            qc.t(q[6])
            qc.t(q[6])
            qc.t(q[6])
            self.num_t_gates[6] += 3
        if self.board1[2] and self.board1[2] == self.board1[6]:
            qc.t(q[4])
            qc.t(q[4])
            qc.t(q[4])
            self.num_t_gates[4] += 3
        if self.board1[4] and self.board1[4] == self.board1[6]:
            qc.t(q[2])
            qc.t(q[2])
            qc.t(q[2])
            self.num_t_gates[2] += 3

        for index, move in enumerate(self.board1):
            if not move:
                qc.h(q[index])
            else:
                # if there is already a move there - don't show that any t gates were applied
                self.num_t_gates[index] = -1
        qc.measure(q, c)

        backend = Aer.get_backend('qasm_simulator')
        shots = 100
        job_sim = execute(qc, backend, shots=shots)
        sim_result = job_sim.result().get_counts(qc)

        counts = [0] * 9

        for key, count in sim_result.items():

            key = key[::-1]
            for index, val in enumerate(key):
                if val == '1':
                    counts[index] += count

        max_count = 0
        max_index = 0
        for index, count in enumerate(counts):
            if not self.board1[index] and count > max_count:
                max_index = index
                max_count = count

        self.move = max_index
