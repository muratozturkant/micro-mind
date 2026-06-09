from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


ALLOWED_STATES = {"ACTIVE", "SLEEPING", "PROMOTED", "DEPRECATED", "ARCHIVED"}


@dataclass
class BaseNode:
    node_name: str
    node_id: str = field(default_factory=lambda: str(uuid4()))
    activation_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    last_execution: str | None = None
    sleep_score: float = 0.0
    fitness_score: float = 0.0
    state: str = "SLEEPING"

    def execute(self, *args, **kwargs):
        raise NotImplementedError

    def run(self, *args, **kwargs):
        self._activate()
        try:
            result = self.execute(*args, **kwargs)
        except Exception:
            self._finish(success=False)
            raise

        self._finish(success=True)
        return result

    def to_dict(self) -> dict:
        return asdict(self)

    def _activate(self) -> None:
        self.activation_count += 1
        self.state = "ACTIVE"
        self.last_execution = datetime.now(UTC).isoformat()

    def _finish(self, success: bool) -> None:
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1

        total = self.success_count + self.failure_count
        self.fitness_score = self.success_count / total if total else 0.0
        self.sleep_score = 1.0 if self.state == "ACTIVE" else self.sleep_score
        self.state = "SLEEPING"
