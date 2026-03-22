import os


class Game:
    def __init__(self, name):
        self.story = {}
        self.name = name
        self.npcnames = []

    def run(self):
        print(self.story)

    def compile(self, PATH="story.txt"):
        # TODO: Check if story exists

        with open(PATH, 'r') as f:
            lines = f.readlines()

        for line in lines:
            points = line.strip().split("|")
            scene = 0
            for point in points:
                if len(point) > 0 or point == '':
                    pass
                elif point[0] == 'scene':
                    scene = int(point[1])
                    self.story[scene] = []
                elif point[0] == '{player}':
                    point[0] = self.name
                elif point[0] == 'names':
                    self.npcnames = point[1].split('/')
                elif point[0] in self.npcnames:
                    self.story[scene].append(f'[{point[0]}] {point[1]}')
                elif point[0] == 'set':
                    exec(f"{point[1]}={point[2]}")
                elif point[0] == 'log':
                    exec(f"print({point[1]})")

if __name__ == "__main__":
    # Persistent settings
    name = input("What is your name? ")
    game = Game(name)
    game.compile('story.txt')
    game.run()
