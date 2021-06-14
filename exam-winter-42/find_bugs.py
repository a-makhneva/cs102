import typing as tp


class WorkflowFixer:
    def __init__(self, filename: str) -> None:
        self.tasklist = self.readf(filename)
        pass

    def readf(self, fname: str) -> list:
        taskarray = []
        with open(fname, "r") as ins:
            for line in ins:
                if line.startswith("task"):
                    task = []  # type: ignore
                    continue
                elif len(line.strip()) == 0:
                    taskarray.append(task)
                    continue
                else:
                    first_letter = line.split("->")[0].strip()
                    second_letter = line.split("->")[1].strip()
                    task.append([first_letter, second_letter])
            # taskarray.append(task)
            return taskarray

    @staticmethod
    def is_valid(mylist: tp.List) -> bool:
        mylist.sort(key=lambda x: x[0])  # Sort by 1st element
        for i in range(len(mylist) - 1):
            if mylist[i][1] != mylist[i + 1][0]:
                return False
        if mylist[0][0] != mylist[len(mylist) - 1][1]:
            return False
        return True

    def try_to_fix(self, mylist: tp.List) -> bool:  # type: ignore
        # if self.is_valid(mylist):
        #     return False  #removing validity check and alphabetical sorting
        fixes_list = []
        for i in range(0, len(mylist) - 1):
            if mylist[i][1] != mylist[i + 1][0]:
                mylist[i][1] = mylist[i + 1][0]
                my_fix = mylist[i]
                fixes_list.append(my_fix)
        if mylist[0][0] != mylist[len(mylist) - 1][1]:
            mylist[len(mylist) - 1][1] = mylist[0][0]
            my_fix = mylist[i + 1]
            fixes_list.append(my_fix)
        if len(fixes_list) == 1:
            print(fixes_list[0][0] + " -> " + fixes_list[0][1])
        else:
            print("V, V, V...")
        pass

    def run(self):
        for i in range(len(self.tasklist)):
            self.try_to_fix(self.tasklist[i])
        pass


if __name__ == "__main__":
    myinstance = WorkflowFixer("tasks.txt")
    myinstance.run()
