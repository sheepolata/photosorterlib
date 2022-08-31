from reprint import output
import time

if __name__ == "__main__":
    with output(output_type='dict') as output_lines:
        for i in range(10):
            output_lines['Moving file'] = "File_{}".format(i)
            for progress in range(100):
                output_lines['Total Progress'] = "[{done}{padding}] {percent}%".format(
                    done = "#" * int(progress/10),
                    padding = " " * (10 - int(progress/10)),
                    percent = progress
                    )
                time.sleep(0.05)