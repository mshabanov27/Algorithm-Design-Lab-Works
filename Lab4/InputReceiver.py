class InputReceiver:
    @staticmethod
    def receive_graph_size():
        print('Enter graph size:')
        number = input()
        while not number.strip().isdigit():
            print('Entered value should be an integer. Try again: ')
            number = input()
        return int(number)

    @staticmethod
    def receive_number_input(graph_size):
        print('Enter maximum number of edges:')
        number = input()
        number_invalid = True
        while number_invalid:
            if not number.strip().isdigit():
                print('Entered value should be an integer. Try again: ')
                number = input()
            elif int(number) >= graph_size:
                print('Entered value should be smaller than graph size. Try again: ')
                number = input()
            elif int(number) > 30:
                print('This program supports only up to 30 colors. Try again: ')
                number = input()
            else:
                number_invalid = False
        return int(number)
