from turtlelsystem.Machine import Machine

#Not much we can do here without user input

def test_bad_command():
    m = Machine()
    assert m.do_command("foobar") == "ERROR: Command not found"
