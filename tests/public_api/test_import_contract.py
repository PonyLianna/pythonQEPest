from pythonQEPest import QEPest, QEPestData, QEPestInput, QEPestOutput


def test_public_api_symbols_are_importable():
    assert QEPest is not None
    assert QEPestInput is not None
    assert QEPestOutput is not None
    assert QEPestData is not None


def test_public_api_compute_smoke():
    model = QEPest()
    payload = QEPestInput(
        name="mol1",
        mol_weight=240.2127,
        log_p=3.2392,
        hbond_acceptors=5,
        hbond_donors=1,
        rotatable_bonds=4,
        aromatic_rings=1,
    )
    result = model.compute_params(payload)

    assert isinstance(result, QEPestOutput)
    assert isinstance(result.data, QEPestData)
    assert result.name == "mol1"
