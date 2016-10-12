## General structure

At the current time, we don't have an interface for non admin users to submit challenges.
But you can still submit challenges, by filling out and mailing us this form and a tester file:

Event:

Title:

Description:

Author:

Timeout:

Points:

\+ my_tests.py file

Email to: kristo.koert@gmail.com

NOTE: You can always ask for help if you don't understand something, but if you want you can just leave some fields empty.

**EXAMPLE**

Event: "Meetup: Collections"

Title: "namedtuple"

Description: 

Slightly improve this code using a namedtuple:


    class DBRowX:
        # I wish I could make the fields immutable in a trivial way..
    
        def __init__(self, this, that, wuut, waat):
            self.this = this
            self.that = that
            self.wuut = wuut
            self.waat = waat
    
    
    def gen_db_row(data):
        """
        :param data: tuple of this, that, wuut, waat
        """
        this, that, wuut, waat = data
        return DBRowX(this, that, wuut, waat)


Author: "kristo.koert@gmail.com"

Tester: "named_tuple_test.py"

Tester file content:

    # NOTE: solution is the users files module, the file they upload
    from solution import gen_db_row
    
    
    class DBRowXOld:
        # I wish I could make the fields immutable in a trivial way..
    
        def __init__(self, this, that, wuut, waat):
            self.this = this
            self.that = that
            self.wuut = wuut
            self.waat = waat
    
    
    def gen_db_row_old(data):
        """
        :param data: tuple of this, that, wuut, waat
        """
        this, that, wuut, waat = data
        return DBRowXOld(this, that, wuut, waat)
    
    data = (1, 2, 3, 4)
    old = gen_db_row_old(data)
    new = gen_db_row(data)
    
    # NOTE: any assertion error, will fail the test case
    
    assert old.this == new.this
    
    assert old.that == new.that
    
    assert old.wuut == new.wuut
    
    assert old.waat == new.waat

DONE!
