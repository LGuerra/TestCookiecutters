from fovissste import validation

schema = {
    "id_avaluo": validation.validate_clve_avaluo,
    "riesgo": validation.validate_riesgo,
    "estatus": validation.validate_estatus,
    "fecha_gte": validation.validate_fecha_gte,
    "fecha_lte": validation.validate_fecha_lte,
    "offset": validation.validate_offset,
    "limit": validation.validate_limit
}


def test_validate_no_errors():
    # All pass
    params = {
        "id_avaluo": "all",
        "riesgo": "1,3",
        "estatus": "2",
        "fecha_gte": "2015-12-17",
        "fecha_lte": "2015-06-17",
        "offset": '1',
        "limit": '1'
    }
    errors = validation.validate(schema, params)
    assert len(errors.keys()) == 0


def test_validate_fail1():
    # Fails: clve_avaluo, riesgo, estatus, fecha_gte, fecha_lte
    params = {
        "id_avaluo": "al",
        "riesgo": "1,",
        "estatus": "",
        "fecha_gte": "20g1512-17",
        "fecha_lte": "2015-06-171",
        "offset": '1',
        "limit": '1'
    }
    errors = validation.validate(schema, params)
    assert len(errors.keys()) == 5
    assert 'id_avaluo' in errors
    assert 'riesgo' in errors
    assert 'estatus' in errors
    assert 'fecha_gte' in errors
    assert 'fecha_lte' in errors


def test_validate_fail2():
    # Fails: riesgo, estatus, fecha_gte, fecha_lte, offset, limit
    params = {
        "id_avaluo": "all",
        "riesgo": "",
        "estatus": "2,4",
        "fecha_gte": "-12-17",
        "fecha_lte": "2015-16-17",
        "offset": '',
        "limit": 'rw'
    }
    errors = validation.validate(schema, params)
    assert len(errors.keys()) == 6
    assert 'riesgo' in errors
    assert 'estatus' in errors
    assert 'fecha_gte' in errors
    assert 'fecha_lte' in errors
    assert 'offset' in errors
    assert 'limit' in errors


def test_validate_fail3():
    # Fails: bbox, id_tipo_propiedad, precio_gte, precio_lte, fecha_gte,
    # 	fecha_lte
    params = {
        "id_avaluo": "all",
        "riesgo": "s,2",
        "estatus": "-1",
        "fecha_gte": "2015-12a-17",
        "fecha_lte": "2015-060-17",
    }
    errors = validation.validate(schema, params)
    assert len(errors.keys()) == 5
    assert 'riesgo' in errors
    assert 'estatus' in errors
    assert 'fecha_gte' in errors
    assert 'fecha_lte' in errors
    assert 'missing' in errors
    assert len(errors['missing']) == 2


def test_validate_multiple_values():
    params = {
        "id_avaluo": "all",
        "riesgo": "1,2,3",
        "estatus": "2,3",
        "fecha_gte": "2015-12-17",
        "fecha_lte": "2015-06-17",
        "offset": '1',
        "limit": '1'
    }
    errors = validation.validate(schema, params)
    assert True
    assert len(errors.keys()) == 0


def test_validate_repeated_values():
    # Fails: bbox, id_tipo_propiedad, edad
    params = {
        "riesgo": '1,1,3',
        "estatus": '1,1,3',
        "limit": '-1',
        "offset": '-2'
    }
    errors = validation.validate(schema, params)
    assert len(errors.keys()) == 3
    assert 'limit' in errors
    assert 'offset' in errors
    assert 'missing' in errors
    assert len(errors['missing']) == 3


def test_validate_extra_param():
    # Pass with extra param
    params = {
        "id_avaluo": "all",
        "riesgo": "1,3",
        "estatus": "2",
        "fecha_gte": "2015-12-17",
        "fecha_lte": "2015-06-17",
        "offset": '1',
        "limit": '1',
        "hi": 'bad'
    }
    errors = validation.validate(schema, params)
    assert True
    assert len(errors.keys()) == 0


def test_validate_allow_paremters_marked_with_all():
    params = {
        "id_avaluo": "all",
        "riesgo": "all",
        "estatus": "all",
        "fecha_gte": "2015-12-17",
        "fecha_lte": "2015-06-17",
        "offset": '1',
        "limit": '1'
    }
    errors = validation.validate(schema, params)
    assert len(errors.keys()) == 0


def test_validate_if_is_member_of_collection():
    smallschema = {
        'allow_empty': validation.validate_allow_empty
    }

    noerrors = validation.validate(smallschema, {'allow_empty': 'true'})
    assert len(noerrors) == 0

    errors = validation.validate(smallschema, {'allow_empty': 'what'})
    assert len(errors) == 1
    assert 'allow_empty' in errors
