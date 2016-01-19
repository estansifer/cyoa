#!/usr/bin/python

import sys

def parse_link(link):
    filename, _, pagename = link.rpartition('|')
    return (filename.strip(), pagename.strip())

class Page:
    def __init__(self, game_file, pagename, raw_body):
        self.game_file = game_file
        self.pagename = pagename
        self.raw_body = raw_body
        self.body = []
        self.links = []

        counter = 1
        for line in raw_body:
            unparsed_line = line
            parsed_line = ""
            while True:
                pre, mid, post = unparsed_line.partition("[[")
                if mid == "":
                    parsed_line += unparsed_line
                    break
                else:
                    link, mid2, post2 = post.partition("]]")
                    if mid2 == "":
                        parsed_line += unparsed_line
                        break
                    else:
                        self.links.append(parse_link(link))
                        unparsed_line = post2
                        parsed_line += pre
                        parsed_line += "("
                        parsed_line += str(counter)
                        parsed_line += ")"
                        counter += 1
            while len(self.body) < 2 and not (parsed_line == ""):
                self.body.append("")
            self.body.append(parsed_line)

        if not (self.body[-1] == ""):
            self.body.append("")

class GameFile:
    def __init__(self, game_files, data):
        self.game_files = game_files
        self.raw_data = data
        self.pages = []
        self.page_dict = {}

        cur_page = []
        cur_page_name = None
        for line in data:
            if len(line) >= 2 and line[0] == '[' and line[-1] == ']':
                if not (cur_page_name is None):
                    page = Page(self, cur_page_name, cur_page)
                    self.pages.append(page)
                    self.page_dict[cur_page_name] = page
                cur_page_name = line[1:-1]
                cur_page = []
            else:
                cur_page.append(line)

        if not (cur_page_name is None):
            page = Page(self, cur_page_name, cur_page)
            self.pages.append(page)
            self.page_dict[cur_page_name] = page

        if len(self.pages) > 0:
            self.page_dict[""] = self.pages[0]

        # Now we go through all pages to verify that there are no missing links.
        for page in self.pages:
            for filename, pagename in page.links:
                if filename == "" and not (pagename in self.page_dict):
                    print ("Missing page \"" + pagename + "\".")

    def get_page(self, pagename):
        page = self.page_dict.get(pagename)
        if page is None:
            print ("Cannot find page \"" + pagename + "\".")
        return page

class GameFiles:
    def __init__(self):
        self.files = []
        self.file_dict = {}

    def load_file(self, filename):
        if not (filename in self.file_dict):
            try:
                f = open(filename)
                data = f.readlines()
                f.close()

                # Trim extraneous endlines
                data2 = []
                for line in data:
                    data2.append(line[:-1])

                game_file = GameFile(self, data2)
                self.files.append(game_file)
                self.file_dict[filename] = game_file
            finally:
                pass

    # returns 'None' if there is any problem with loading the file
    def get_game_file(self, filename):
        self.load_file(filename)
        return self.file_dict.get(filename)

    def get_page(self, filename, pagename):
        game_file = self.get_game_file(filename)
        if game_file is None:
            print ("Cannot find file \"" + filename + "\".")
            return None
        return game_file.get_page(pagename)

quit_program = object()
previous_page = object()

class TextDisplay:
    def __init__(self, page_size = 50):
        self.page_size = page_size

    def start(self):
        pass

    def end(self):
        pass

    # returns
    #   quit_program - if the player wants to quit
    #   previous_page - if the player wants to go backwards one step
    #   p - if the player wants to go to page 'p'
    #
    # User types a number to go to that page
    # 'back' to go to the previous page
    # 'exit' or 'quit' to exit
    # 'help' to go to the help page
    # 'refresh' to display the prompt again.
    #
    def display_page(self, page):
        def link_index(i):
            game_file = page.game_file
            filename, pagename = page.links[i - 1]
            if filename == "":
                return game_file.get_page(pagename)
            else:
                return game_file.game_files.get_page(filename, pagename)

        while True:
            for i in range(0, len(page.body)):
                if i > 0 and i + 1 < len(page.body) and (i % self.page_size) == 0:
                    try:
                        input ("[[Press enter to continue.]]")
                    except:
                        print ("")
                        return quit_program
                print (page.body[i])

            while True:
                try:
                    choice = input ("> ")
                except:
                    print ("")
                    return quit_program

                if len(choice) == 0:
                    if len(page.links) == 1:
                        new_page = link_index(1)
                        if not (new_page is None):
                            return new_page
                elif choice[0] == 'r':
                    break
                elif choice[0] == 'b':
                    return previous_page
                elif choice[0] == 'q' or choice[0] == 'e':
                    return quit_program
                elif choice[0] == 'h':
                    game_files = page.game_file.game_files
                    new_page = game_files.get_page("games/help", "")
                    return new_page
                elif choice.isdigit():
                    i = int(choice)
                    if i >= 1 and i <= len(page.links):
                        new_page = link_index(i)
                        if not (new_page is None):
                            return new_page
                    else:
                        if len(page.links) == 0:
                            print ("There are no choices. Type \"back\" to go back, \"quit\" to quit, or \"help\" for help.")
                        elif len(page.links) == 1:
                            print ("Choice " + choice + " is unavailable. This is only one choice. (Pressing 'enter' will continue with the only choice.)")
                        else:
                            print ("Choice " + choice + " is unavailable. There are only " + str(len(page.links)) + " choices.")
                else:
                    print ("I did not understand \"" + choice + "\". Type \"help\" for help.")

        return quit_program

def main_loop(display, start_page):
    display.start()

    page_history = [start_page]

    while True:
        cur_page = page_history[-1]
        next_page = display.display_page(cur_page)
        if next_page is quit_program:
            break
        elif next_page is previous_page:
            if len(page_history) > 1:
                page_history.pop()
        else:
            page_history.append(next_page)

    display.end()

def main():
    num_args = len(sys.argv) - 1

    if num_args == 0:
        filename = "menu"
        pagename = ""
    elif num_args == 1:
        filename = sys.argv[1]
        pagename = ""
    elif num_args == 2:
        filename = sys.argv[1]
        pagename = sys.argv[2]

    game_files = GameFiles()

    main_loop(TextDisplay(), game_files.get_page(filename, pagename))

main()
