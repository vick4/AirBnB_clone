#!/usr/bin/python3
"""This is a command interpreter for the AirBnB_clone project"""


import cmd
import os
import sys

from models.base_model import BaseModel
from models import storage, user, place, state, city, amenity, review


class HBNBCommand(cmd.Cmd):
    """
    A command interpreter that prints a prompt to the console
    for the AirBnB Project
    """

    # custom prompt to print if in interactive mode
    prompt = "(hbnb) " if sys.stdin.isatty() else ''

    # Dictionary mapping class names to their corresponding classes
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Place': Place,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Review': Review
    }

    # List of dot commands supported by the console
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']

    def precmd(self, line):
        """
        Precommand Hook

        This method is called just before the command is executed.
        It reformats the command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in the usage example.)
        """
        _cmd = _cls = _id = _args = ''  # Initialize line elements

        # Scan for general formatting - i.e., '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # Parse line from left to right
            pline = line[:]  # Parsed line

            # Isolate <class name>
            _cls = pline[:pline.find('.')]

            # Isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # Passing parenthenses that contains arguments
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # Partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline converts to tuple

                # Isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')

                # If arguments exist beyond _id
                pline = pline[2].strip()  # pline is now a string
                if pline:
                    # Check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """
        Postcommand Hook

        This method is called just after the command is executed.
        It prints the prompt if the input stream is not
        connected to a terminal.

        """
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, arg):
        """Quit command to exit the program\n"""
        return True

    def do_EOF(self, arg):
        """Handles the command of "End Of File" to exit the program"""
        exit(0)

    def emptyline(self):
        pass

    def do_create(self, args):
        """
        Create Command.

        Creates a new instance of a Class.
        """
        try:
            cls = globals()[BaseModel]
            new_instance = BaseModel()
            new_instance.save()
            print(new_instance.id)
        except KeyError:
            print("** class name missing **")
        except NameError:
            print("class doesn't exist")

    def do_show(self, args):
        """
        Show Command.

        prints the string representation of an instance based on the...
                ...class name and id
        Usage: show <className> <objectId>
        """
        new = args.partition(" ")
        cls_name = new[0]
        cls_id = new[2]

        # Guard against trailing args
        if cls_id and ' ' in cls_id:
            cls_id = cls_id.partition(' ')[0]

        if not cls_name:
            print("** class name missing **")
            return

        if cls_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not cls_id:
            print("** instance id missing **")
            return

        key = cls_name + "." + cls_id
        try:
            print(storage.all()[key])
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        """
        Destroys a specified object.

        Usage: destroy <className> <objectId>
        """

        new = args.partition(" ")
        cls_name = new[0]
        cls_id = new[2]
        if cls_id and ' ' in cls_id:
            cls_id = cls_id.partition(' ')[0]

        if not cls_name:
            print("** class name missing **")
            return

        if cls_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not cls_id:
            print("** instance id missing **")
            return

        key = cls_name + "." + cls_id

        try:
            storage.delete(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def do_all(self, args):
        """
        Prints all string representation of all instances based or not on...
                        ...the class
        """
        print_list = []

        if args:
            args = args.split(' ')[0]  # Remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all().items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage.all().items():
                print_list.append(str(v))

        print(print_list)

    def do_update(self, args):
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
