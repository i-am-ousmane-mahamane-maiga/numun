import golly as g

g.new("MyCA")
g.setrule("Life")
g.putcells([[1,0],[2,1],[0,2],[1,2],[2,2]])  # A glider
g.update()
g.step()  # Advance one generation