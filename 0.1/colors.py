from random import *

colors = dict()

def SetColors():
	colors["green"] = (91,194,64)
	colors["red"]   = (255,51,51)
	colors["blue"]  = (102,153,255)
	colors["orange"] = (255,69,0)
	colors["hgreen"] = (34,139,34)
	colors["lblue"] = (72,209,204)

def randomColor():
	if len(colors.keys()) == 0:
		return (100,0,100)
	keys = colors.keys()

	rand = randrange(len(keys))

	value = colors[keys[rand]]
	del colors[keys[rand]]

	return value


if __name__ == "__main__":
	print randomColor()