import os
class Menu:
    def __init__(self):
        pass
    def clear_screen(self):
        os.system("clear")

    def _show_menu_and_get_selection(self):
        self.clear_screen()
        menu_text = """
    Welcome to the TrainLineApp App!
    Here you can view all the latest train timetable information and plan your journeys accordingly. 
    Please, select an option below by entering a number:
        [1] Plan your journey
        [2] Show table
        [3] Play the quiz!
        [4] Exit
        """
        print(menu_text)
        while True:
            try:
                return int(input("Enter a number: "))
            except ValueError:
                print("Please enter a valid number.")