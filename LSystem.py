class LSystemOverflow(Exception):
    """
    Exception that happens when
    an LSystem generates a string
    that's too long. This helps
    limit memory usage.
    """
    pass

class LSystem(object):
    """
    Class that handles an Lindenmayer System (L-System)
    """
    def __init__(self, start, rules, overflow_length=10000):
        """
        Algae example:

        start = "A"
        rules = {
            "A": "AB",
            "B": "A"
        }

        :param str start: the start string
        :param dict rules: Substitution rules
            {str -> str} where the keys
            are single characters.
        :param int overflow_length: maximum length for
            each iteration's strings before raising an
            LSystemOverflow exception. This helps limit
            memory usage.
        """
        self.start = start
        self.rules = rules
        self.overflow_length = overflow_length

    def __iter__(self):
        """
        infinite iterator for this L-System.
        The 0th yield is the start string
        Every subsequent yield is an iteration of the system.

        :returns: a generator of each iteration of
            the L-System
        :rtype: generator of strings
        """
        current = self.start
        yield current
        while True:
            tmp = ""

            for ch in current:
                tmp += self.rules.get(ch, ch)
            current = tmp

            if len(current) > self.overflow_length:
                break

            yield current

        #L-System has generated a string that's too large.
        raise LSystemOverflow

    def nth(self, n):
        """
        Get the n-th iteration of this L-System. this
        is just a convenience method based on how
        L-Systems are used.

        :param int n: Number of iteration. 0 means
        :raises: LSystemOverflow if
        """
        gen = iter(self)

        #extract the 0th iteration
        current = next(gen)

        #Continue to extract iterations
        for i in xrange(n):
            current = next(gen)
        
        return current
