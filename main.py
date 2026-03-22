import os


class Game:
    def __init__(self):
        pass

    def run(self):
        pass

    def compile(self, PATH="story.txt"):
        # TODO: Check if story exists

        with open('story.txt', 'r') as f:
            lines = f.readlines()

        for line in lines:
            points = line.split("|")
            print(points)


if __name__ == "__main__":
    game = Game()
    game.compile('story.txt')
