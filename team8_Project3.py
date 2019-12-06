import dissasembler
import simulator

mydis = dissasembler.dissasembler()
output = {}
output = mydis.run()
mydis.print()

mysim = simulator.simClass(**output)
mysim.run()