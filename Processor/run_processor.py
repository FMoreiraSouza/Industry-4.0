from modules.Observable import *
from modules.Observer import *
from strategiesProcessor.strategyTags import Processor
if __name__ == "__main__":
  # context = Context(Processor())
  # context.do_some_business_logic()

  subject = ConcreteSubject()

  observer_a = RunProcessor(Processor())
  subject.attach(observer_a)
  subject.data_pre_processing_logic()