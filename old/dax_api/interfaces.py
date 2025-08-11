from abc import ABC, abstractmethod
from typing import Optional


class IDataService(ABC):
    @abstractmethod
    def get_data(self, container_name: str, file_name: str) -> bytes:
        pass

    @abstractmethod
    def upload_data(
        self,
        container_name: str,
        file_name: str,
        data: bytes,
        overwrite: Optional[bool],
    ) -> None:
        pass

    @abstractmethod
    def delete_data(self, container_name: str, file_name: str) -> None:
        pass

    @abstractmethod
    def list_data(self, container_name: str) -> list[str]:
        pass
