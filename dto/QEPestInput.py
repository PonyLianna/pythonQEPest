from pydantic import BaseModel


class QEPestInput (BaseModel):
    name: str = ""

    mol_weight: float = 0.0
    log_p: float = 0.0

    hbond_acceptors: int = 0
    hbond_donors: int = 0

    rotatable_bonds: int = 0
    aromatic_rings: int = 0
