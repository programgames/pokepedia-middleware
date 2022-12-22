from middleware.exception import InvalidConditionException
from pokeapi.pokemon_v2.models import Machine


def is_hm(machine: Machine, gen: int) -> bool:
    if 1 <= machine.machine_number <= 99 and gen <= 6:
        return __is_hm_machine(machine)
    elif gen <= 6 and machine.machine_number == 100:
        return False
    elif gen <= 6 and machine.machine_number >= 101:
        return __is_hm_machine(machine)
    elif gen == 7:
        return False
    elif gen == 8:
        return __is_hm_machine(machine)
    else:
        raise InvalidConditionException(f'Impossible to know if machine number {machine.machine_number} is an hm or '
                                        f'not')

def __is_hm_machine(machine: Machine) -> bool:
    u"""True if this machine is a HM, False if it's a TM."""
    return machine.machine_number >= 100
