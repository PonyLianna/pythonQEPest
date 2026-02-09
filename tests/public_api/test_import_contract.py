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
        mol_weight=308.354,
        log_p=2.1086,
        hbond_acceptors=2,
        hbond_donors=1,
        rotatable_bonds=4,
        aromatic_rings=1,
    )

    result = model.compute_params(payload)

    assert isinstance(result, QEPestOutput)
    assert isinstance(result.data, QEPestData)

    assert result.name == "mol1"
    assert result.data == QEPestData(qe_h=0.9357, qe_i=0.7146, qe_f=0.8022)
