        
        for i in range(self.width*self.height):
            x, y = i//self.height, i//self.width
            curr_square = self.array[x][y]
            if x != self.width - 1:
                curr_square.r = self.array[x+1][y]
                curr_square.r.l = curr_square
                curr_square.cluster.append(curr_square.r)
            elif x != 0:
                curr_square.l = self.array[x-1][y]
                curr_square.l.r = curr_square
                curr_square.cluster.append(curr_square.l)
            if y != 0:
                curr_square.u = self.array[x][y-1]
                curr_square.u.d = curr_square
                curr_square.cluster.append(curr_square.u)
                if x != 0:
                    curr_square.ul = self.array[x-1][y-1]
                    curr_square.ul.dr = curr_square
                    curr_square.cluster.append(curr_square.ul)
                if x != self.width - 1:
                    curr_square.ur = self.array[x+1][y-1]
                    curr_square.ur.dl = curr_square
                    curr_square.cluster.append(curr_square.ur)
        