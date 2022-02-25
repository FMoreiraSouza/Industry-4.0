from modules.Observable import *
from modules.Observer import *
if __name__ == "__main__":
    # context = Context(Processor())
    # context.do_some_business_logic()

    subject = ConcreteSubject()
    observer_a = RunProcedure()
    subject.attach(observer_a)
    subject.data_analysis_logic()