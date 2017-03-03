class Task(object):
    """docstring for Task.  Task is designed to store task information
        derived from the logbook.csv via the logger.  Task provides print
        formatting via __str__ and editing functions"""
    def __init__(self, **kwargs):
        super(Task, self).__init__()
        self.id = kwargs.get('id')
        self.date = kwargs.get('date')
        self.name = kwargs.get('name')
        self.time_spent = kwargs.get('time_spent')
        self.general_notes = kwargs.get('general_notes')

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return "{0!s:<20s}{1!s:<20s}{2!s:<20s}{3!s:<20s}".format(
                                                self.date,
                                                self.name,
                                                self.time_spent,
                                                self.general_notes
                                                )

    def __format__(self, format):
        width = 20
        precision = 15
        if (format == 'list-display'):
            return "{0!s:<20s}{1!s:<20s}{2!s:<20s}{3!s:<20s}".format(
                                                    self.date,
                                                    self.name,
                                                    self.time_spent,
                                                    self.general_notes
                                                    )
        elif (format == 'edit_display'):
            return (
                "-------------------------------------------------------------"
                "--------------------\n{5!s:^80}"
                "\n\tId: {4!s:>3}\n\t---------\n"
                "\tDate: {0!s:<20s}\n\tName: {1!s:<20s}"
                "\n\tDuration: {2!s:<20s}\n\tNotes: {3!s:<20s}".format())

        return (
                "-----------------------------------------------------------\n"
                "Date: {}\n".format(self.date) +
                "      Name:  {}\n".format(self.name) +
                "Time Spent:  {}\n".format(self.time_spent) +
                "     Notes:  {}\n".format(self.general_notes)
                )

    def edit(self):
        """generator that prompts user and passes the response for each of the
        task attributes"""
