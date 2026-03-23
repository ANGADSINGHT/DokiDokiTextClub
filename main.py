import asyncio
from subprocess import call
from random import choice
from os import name as osname


DEBUG = False

bug_callouts = [
    'A bug? In my code!?',
    'Naah I hate coding',
    'Sybau you did something wrong for it to crash',
    'Damn I made a mistake :(',
    "Idfk I ain't fixing this bug"
]


def clear_screen():
    call(['clear' if osname != 'nt' else 'cls'], shell=True)


async def print_slow(text, delay=0.1):
    for ch in text:
        print(ch, end="", flush=True)
        await asyncio.sleep(delay)
    print(end="")


class Game:
    def __init__(self, name):
        self.story = {}
        self.name = name
        self.npcnames = []
        self.scene = 1
        self.running = False

    async def run(self):
        self.running = True

        if DEBUG:
            print(f"Full story: \n{self.story}")

        while self.running:
            clear_screen()

            choices = []
            scene_changed = False   # ← add this

            for line in self.story[self.scene]:

                if line.isnumeric():
                    self.scene = int(line)
                    scene_changed = True
                    break

                elif line.startswith("CHOICE"):
                    txt, nextscene = line.split('|', 1)
                    dialog = txt[7:].replace(']', ' =').replace(':', self.name)
                    print(f">> {dialog}")
                    choices.append(int(nextscene))

                elif any(line.startswith(f'[{name}]') for name in self.npcnames):  # noqa: E501

                    line = line.replace(":", self.name)

                    await print_slow(line, 0.01)
                    input()

                else:
                    print(line)

            # ✅ restart loop if we jumped to another scene
            if scene_changed:
                continue

            if not choices:
                self.running = False
                break

            while True:
                choice_input = input("Choice: ")
                if choice_input.isnumeric():
                    choice_num = int(choice_input) - 1
                    if 0 <= choice_num < len(choices):
                        self.scene = choices[choice_num]
                        break
                    else:
                        print("Invalid choice.")
                else:
                    print("Please enter a number.")

    def compile(self, PATH="story.txt"):
        # TODO: Check if story exists

        with open(PATH, 'r') as f:
            lines = f.readlines()

        scene = 0
        for line in lines:
            line = line.strip()
            if not line or line.startswith('note'):
                continue
            parts = line.split("|")
            if len(parts) < 1:
                continue
            cmd = parts[0]
            if cmd == 'scene':
                scene = int(parts[1])
                self.story[scene] = []
            elif cmd == 'names':
                self.npcnames = parts[1].split('/')
            elif cmd in self.npcnames:
                if cmd == 'player':
                    cmd = self.name
                self.story[scene].append(f'[{cmd}] {parts[1]}')
            elif cmd == 'choice':
                options = parts[1].split('/')
                next_scenes = parts[2].split('/')
                for i in range(len(options)):
                    self.story[scene].append(f"CHOICE[{i+1}] {options[i]}|{next_scenes[i]}")  # noqa: E501
            elif cmd == 'forward':
                self.story[scene].append((parts[1]))
            else:
                if len(parts) > 1:
                    self.story[scene].append(parts[1])


def main(name):
    try:
        game = Game(name)
        print("Compiling story...")

        game.compile('story.txt')

        print("-"*67)
        if not DEBUG:
            clear_screen()

        asyncio.run(game.run())
        return 1
    except Exception as e:
        if DEBUG:
            print("Looks like the game is crashing... lemme help you out!")
            print(f"self.scene={game.scene}")
            input("Press enter to raise the error and quit...")
            raise e
        return print(f"Failed to compile! Error: {e}")


if __name__ == "__main__":
    # Persistent settings
    name = input("What is your name? ")

    if main(name) != 1:
        print(choice(bug_callouts))
