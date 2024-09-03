from middleware.exception import InvalidConditionException
from pokeapi.db.tables import Machine


def is_hm(machine: Machine, gen: int) -> bool:
    if 1 <= machine.machine_number <= 99 and gen <= 6:
        return machine.is_hm
    elif gen <= 6 and machine.machine_number == 100:
        return False
    elif gen <= 6 and machine.machine_number >= 101:
        return machine.is_hm
    elif gen == 7:
        return False
    elif gen == 8:
        return machine.is_hm
    else:
        raise InvalidConditionException(f'Impossible to know if machine number {machine.machine_number} is an hm or '
                                        f'not')
