from abc import ABC, abstractmethod

from app.llm.analysis import MessageAnalysis


class LLMService(ABC):

    @abstractmethod
    def analyze(
        self,
        subject: str,
        body: str
    ) -> MessageAnalysis:
        pass