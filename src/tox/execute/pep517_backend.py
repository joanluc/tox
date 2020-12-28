"""A executor that reuses a single subprocess for all backend calls (saving on python startup/import overhead)"""
from pathlib import Path
from threading import Lock
from types import TracebackType
from typing import Dict, Optional, Sequence, Tuple, Type

from tox.execute import ExecuteRequest
from tox.execute.api import Execute, ExecuteInstance, ExecuteStatus
from tox.execute.local_sub_process import LocalSubProcessExecuteInstance
from tox.execute.request import StdinSource
from tox.execute.stream import SyncWrite


class LocalSubProcessPep517Executor(Execute):
    """Executor holding the backend process"""

    def __init__(self, colored: bool, cmd: Sequence[str], env: Dict[str, str], cwd: Path):
        super().__init__(colored)
        self.cmd = cmd
        self.env = env
        self.cwd = cwd
        self._local_execute: Optional[Tuple[LocalSubProcessExecuteInstance, ExecuteStatus]] = None

    def build_instance(self, request: ExecuteRequest, out: SyncWrite, err: SyncWrite) -> ExecuteInstance:
        return LocalSubProcessPep517ExecuteInstance(request, out, err, self.local_execute)

    @property
    def local_execute(self) -> Tuple[LocalSubProcessExecuteInstance, ExecuteStatus]:
        if self._local_execute is None:
            request = ExecuteRequest(cmd=self.cmd, cwd=self.cwd, env=self.env, stdin=StdinSource.API)

            instance = LocalSubProcessExecuteInstance(
                request,
                out=SyncWrite(name="pep517-out", target=None, color=None),  # not enabled no need to enter/exit
                err=SyncWrite(name="pep517-err", target=None, color=None),  # not enabled no need to enter/exit
                on_exit_drain=False,
            )
            self._local_execute = instance, instance.__enter__()
        return self._local_execute

    @staticmethod
    def _handler(into: bytearray, content: bytes) -> None:
        """ignore content generated"""
        into.extend(content)  # pragma: no cover

    def close(self) -> None:
        if self._local_execute is not None:  # pragma: no branch
            execute, status = self._local_execute
            execute.__exit__(None, None, None)
            if execute.process is not None:  # pragma: no branch
                if execute.process.returncode is None:  # pragma: no cover
                    execute.process.terminate()  # pragma: no cover  # if does not stop on its own kill it


class LocalSubProcessPep517ExecuteInstance(ExecuteInstance):
    """A backend invocation"""

    def __init__(
        self,
        request: ExecuteRequest,
        out: SyncWrite,
        err: SyncWrite,
        instance_status: Tuple[LocalSubProcessExecuteInstance, ExecuteStatus],
    ):
        super().__init__(request, out, err)
        self._instance, self._status = instance_status
        self._lock = Lock()

    @property
    def cmd(self) -> Sequence[str]:
        return self._instance.cmd

    def __enter__(self) -> ExecuteStatus:
        self._lock.acquire()
        self._swap_out_err()
        return self._status

    def __exit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        self._swap_out_err()
        self._lock.release()

    def _swap_out_err(self) -> None:
        out, err = self._out, self._err
        # update status to see the newly collected content
        self._out, self._err = self._instance.set_out_err(out, err)
        # update the thread out/err
        self._status.set_out_err(out, err)

    def interrupt(self) -> int:
        return self._instance.interrupt()  # pragma: no cover # just crash instantly