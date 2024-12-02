#!/usr/bin/python3
matrix = list()
start = tuple()

def fillmap(starting_step,frame,steps):
	global matrix
	global start
	pos = set()
	pos.add(start)
	
	for i in range(steps):
		npos = set()
		for p in pos:
			x = p[0]
			y = p[1]
			for xm,ym in zip((-1,0,1,0),(0,-1,0,1)):
				if matrix[(y+ym)%len(matrix)][(x+xm)%len(matrix[0])] == '.':
					npos.add((x+xm,y+ym))				
		pos = npos

		if i%frame == starting_step-1:
			yield len(pos)
	return


def main(input_file,steps):
	global matrix
	global start
	matrix = list()
	start = tuple()
	with open(input_file) as f:
		for y,line in enumerate(f.readlines()):
			matrix.append(list())
			for x,char in enumerate(line.rstrip()):
				if char == 'S':
					start = (x,y)
					matrix[y].append('.')
				else:
					matrix[y].append(char)

	dim = len(matrix)
	a = list()
	
	for res in fillmap(dim//2,dim,dim*2+dim//2+1):
		a.append(res)

	i = dim
	s = a[1]-a[0] 
	r = a[2]-a[1]
	d = r - s
	res = a[1]
	
	while i != steps-dim//2:
		i += dim
		res += r
		r += d
	return res
	
if __name__ == "__main__":
	print(main("input.txt",26501365))
