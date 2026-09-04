from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseCollector(ABC):
    @abstractmethod
    def collect(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Collect data from the source.
        Should return a list of dictionaries representing raw records.
        Each record should contain at least:
        - platform
        - source_url
        - author
        - content
        - date
        - rating (optional)
        - metadata (optional dict)
        """
        pass
