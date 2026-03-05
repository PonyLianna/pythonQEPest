import logging
from typing import Union

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class QEPestInput(BaseModel):
    name: str = ""

    mol_weight: float = 0.0
    log_p: float = 0.0

    hbond_acceptors: int = 0
    hbond_donors: int = 0

    rotatable_bonds: int = 0
    aromatic_rings: int = 0

    @classmethod
    def from_array(cls, data: Union[list, tuple, set]):
        if len(data) != 7:
            raise ValueError(f"Expected 7 elements, got {len(data)}")
        return cls(
            name=data[0],
            mol_weight=float(data[1]),
            log_p=float(data[2]),
            hbond_acceptors=int(data[3]),
            hbond_donors=int(data[4]),
            rotatable_bonds=int(data[5]),
            aromatic_rings=int(data[6]),
        )

    @classmethod
    def from_smiles(cls, smiles: str, name: str = ""):
        try:
            from rdkit import Chem
            from rdkit.Chem import Descriptors
        except ImportError:
            logger.warn(
                "RDKit is not installed. Install it with: poetry install --with rdkit. "
                "Returning QEPestInput with default values."
            )
            return cls(name=name)

        mol = Chem.MolFromSmiles(smiles)

        if mol is None:
            raise ValueError(f"Invalid SMILES: {smiles}")

        return cls(
            name=name,
            mol_weight=Descriptors.ExactMolWt(mol),
            log_p=Descriptors.MolLogP(mol),
            hbond_acceptors=Descriptors.NumHAcceptors(mol),
            hbond_donors=Descriptors.NumHDonors(mol),
            rotatable_bonds=Descriptors.NumRotatableBonds(mol),
            aromatic_rings=Descriptors.NumAromaticRings(mol),
        )
