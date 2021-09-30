from pokedex.db.tables import Machine


def is_hm(machine: Machine, gen: int) -> bool:
    if 1 <= machine.machine_number <= 99 and gen <= 6:
        return machine.is_hm
    elif gen <= 6 and machine.machine_number == 100:
        return False
    elif gen <= 6 and machine.machine_number >= 101:
        return machine.is_hm
    elif gen == 7:
        return False
    elif gen == 8 and machine.machine_number >= 101:
        return machine.is_hm
    elif gen == 8 and machine.machine_number <= 100:
        return False
    else:
        raise RuntimeError('Unknow condition')
