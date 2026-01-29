class CourseDistribution:
    def __init__(self, a_rate, pass_rate, withdrawal_rate):
        self.a_rate = a_rate
        self.pass_rate = pass_rate
        self.withdrawal_rate = withdrawal_rate

    def __str__(self):
        return "A rate: " + str(self.a_rate) + " | Pass rate: " + str(self.pass_rate) + " | Withdrawal rate: " + str(self.withdrawal_rate)
    