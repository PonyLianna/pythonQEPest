from pydantic import BaseModel


class QEPestInput(BaseModel):
    name: str = ""

    mol_weight: float = 0.0
    log_p: float = 0.0

    hbond_acceptors: int = 0
    hbond_donors: int = 0

    rotatable_bonds: int = 0
    aromatic_rings: int = 0

    @classmethod
    def from_array(cls, data: list):
        if len(data) != 7:
            raise ValueError(f"Expected 7 elements, got {len(data)}")
        return cls(
            name=data[0],
            mol_weight=float(data[1]),
            log_p=float(data[2]),
            hbond_acceptors=int(data[3]),
            hbond_donors=int(data[4]),
            rotatable_bonds=int(data[5]),
            aromatic_rings=int(data[6])
        )
