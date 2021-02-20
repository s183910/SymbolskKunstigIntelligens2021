# Add this method to the HospitalState class in src/domains/hospital/state.py
# Allow printing a state directly, i.e. print(state, file=sys.stderr)

    def __repr__(self):
        lines = []
        lookup_table = {}
        for (position, agent_char) in self.agent_positions:
            lookup_table[position] = agent_char
        for (position, box_char) in self.box_positions:
            lookup_table[position] = box_char

        for row in range(len(self.level.walls)):
            line = []
            for col in range(len(self.level.walls[row])):
                position = (row, col)
                if position in lookup_table:
                    line.append(lookup_table[position])
                elif self.level.walls[row][col]:
                    line.append('+')
                else:
                    line.append(' ')
            lines.append(''.join(line))
        return '\n'.join(lines)