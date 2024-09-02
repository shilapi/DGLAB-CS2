from os import mkdir, path


class LogFile:
    def __init__(self, timestamp):
        if not path.exists("./logs"):
            mkdir("./logs")  # Create a logs folder, if it not exists at first launch
        self.name = str(timestamp).replace(" ", "_").replace(":", "-")
        # print(self.name)
        self.path = "logs/" + self.name + ".txt"
        self.create_file()

    def create_file(self):
        file = open(self.path, "w")
        file.write("Log file created at " + self.name + "\n")
        file.close()

    def log_event(self, timestamp, event):
        file = open(self.path, "a")
        file.write(timestamp + "\n")
        file.write(str(event))
        file.write("\n")
        file.close()
